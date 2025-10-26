// src/api.js

const API_BASE_URL = 'https://tkutpalvb5.execute-api.us-east-1.amazonaws.com/default';

/* ---------------- helpers ---------------- */
const num = (v) => {
  if (v == null) return 0;
  if (typeof v === 'number') return v;
  const n = parseFloat(v);
  return Number.isFinite(n) ? n : 0;
};

function unwrapBody(data) {
  if (data && typeof data === 'object' && 'body' in data) {
    return typeof data.body === 'string' ? JSON.parse(data.body) : data.body;
  }
  return data;
}

// If the API ever returns raw DynamoDB Item shapes, unmarshal a few fields we care about:
function unmarshalAttrMap(m = {}) {
  const getS = (k) => m?.[k]?.S ?? undefined;
  const getN = (k) => (m?.[k]?.N != null ? Number(m[k].N) : undefined);
  return {
    student_id: getS('student_id'),
    first: getS('first'),
    last: getS('last'),
    email: getS('email'),
    company: getS('company'),
    total_points: getN('total_points'),
    attendance_points: getN('attendance_points'),
    bonus_points: getN('bonus_points'),
    updated_at: getS('updated_at'),
    // if your table ever stores this
    missed_sessions: getN('missed_sessions'),
  };
}

function looksLikeAttrMap(obj) {
  if (!obj || typeof obj !== 'object') return false;
  // crude check: any value is an object with S/N/BOOL
  return Object.values(obj).some(
    (v) => v && typeof v === 'object' && (('S' in v) || ('N' in v) || ('BOOL' in v))
  );
}

function normalizeStudent(s = {}) {
  const base = looksLikeAttrMap(s) ? unmarshalAttrMap(s) : s;

  return {
    student_id: base.student_id ?? base.id ?? null,
    first: base.first ?? base.first_name ?? '',
    last: base.last ?? base.last_name ?? '',
    email: base.email ?? '',
    company: base.company ?? '',
    total_points: num(base.total_points ?? base.points),
    attendance_points: num(base.attendance_points ?? base.attendance),
    bonus_points: num(base.bonus_points ?? base.bonus),
    missed_sessions: num(base.missed_sessions),  // <-- keep it
    updated_at: base.updated_at ?? base.updated ?? null,

    // Keep any extra fields your backend might add in the future:
    ...Object.fromEntries(
      Object.entries(base).filter(([k]) =>
        ![
          'student_id','id','first','first_name','last','last_name','email','company',
          'total_points','points','attendance_points','attendance','bonus_points','bonus',
          'missed_sessions','updated_at','updated'
        ].includes(k)
      )
    )
  };
}

function toNormalizedArray(payload) {
  if (Array.isArray(payload)) return payload.map(normalizeStudent);
  if (Array.isArray(payload?.students)) return payload.students.map(normalizeStudent);
  if (Array.isArray(payload?.Items)) return payload.Items.map(unmarshalAttrMap).map(normalizeStudent);
  if (payload && typeof payload === 'object' && (payload.first || payload.last)) return [normalizeStudent(payload)];
  return [];
}

/* ---------------- API calls ---------------- */

export async function getLeaderboards() {
  const url = `${API_BASE_URL}/leaderboard`;
  console.log('Fetching leaderboard from:', url);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  const unwrapped = unwrapBody(await res.json());
  const normalized = toNormalizedArray(unwrapped);
  console.log('Leaderboard (normalized):', normalized);
  return normalized;
}

export async function searchStudents(query) {
  // NOTE: If your backend uses body { input_name }, you might need to POST instead.
  const url = `${API_BASE_URL}/search?q=${encodeURIComponent(query)}`;
  console.log('Searching students with query:', query, '→', url);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  const unwrapped = unwrapBody(await res.json());
  const normalized = toNormalizedArray(unwrapped);
  console.log('Search (normalized):', normalized);
  return normalized;
}

export async function createEvent(eventData) {
  const url = `${API_BASE_URL}/sessions`;
  console.log('Creating event →', url, eventData);
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(eventData),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  const unwrapped = unwrapBody(await res.json());
  return unwrapped;
}
