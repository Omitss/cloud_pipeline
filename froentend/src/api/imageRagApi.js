/**
 * 음식 사진을 업로드해 유사한 음식 이미지를 검색한다.
 * @param {{ file: File, topK?: number }} params
 * @returns {Promise<{ query_caption: string, results: Array }>}
 */
export async function searchSimilarFood({ file, topK = 5 }) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('top_k', String(topK))

  const res = await fetch('/imagerag/search', {
    method: 'POST',
    body: formData,
  })

  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new Error(body?.detail || `검색 요청에 실패했습니다. (${res.status})`)
  }

  return res.json()
}
