// 백엔드 이미지가 서빙되는 origin. 개발 중에는 vite 프록시로 /imagerag 요청만 우회하고,
// 이미지(<img src>)는 프록시를 타지 않으므로 백엔드 절대 주소를 그대로 사용한다.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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

/** 검색 결과의 image_path(서버 로컬 경로)를 브라우저에서 볼 수 있는 URL로 변환한다. */
export function getResultImageUrl(dishName, imagePath) {
  const fileName = imagePath.split(/[\\/]/).pop()
  return `${API_BASE_URL}/images/${encodeURIComponent(dishName)}/${encodeURIComponent(fileName)}`
}
