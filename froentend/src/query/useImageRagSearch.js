import { useMutation } from '@tanstack/react-query'
import { searchSimilarFood } from '../api/imageRagApi'

/** 이미지 업로드는 매 호출마다 다른 파일을 검색하는 동작이므로 useQuery가 아닌 useMutation을 사용한다. */
export function useImageRagSearch() {
  return useMutation({
    mutationFn: searchSimilarFood,
  })
}
