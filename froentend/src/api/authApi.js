async function parseErrorOrThrow(res, fallbackMessage) {
  if (res.ok) return
  const body = await res.json().catch(() => null)
  throw new Error(body?.detail || `${fallbackMessage} (${res.status})`)
}

export async function signup({ email, password, nickname }) {
  const res = await fetch('/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, nickname }),
  })
  await parseErrorOrThrow(res, '회원가입에 실패했습니다.')
  return res.json()
}

export async function login({ email, password }) {
  const res = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  await parseErrorOrThrow(res, '로그인에 실패했습니다.')
  return res.json()
}

export async function fetchMe(accessToken) {
  const res = await fetch('/auth/me', {
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  await parseErrorOrThrow(res, '인증 정보를 불러오지 못했습니다.')
  return res.json()
}
