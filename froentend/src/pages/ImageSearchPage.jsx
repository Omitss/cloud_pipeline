import { useRef, useState } from 'react'
import styled from 'styled-components'
import { useImageRagSearch } from '../query/useImageRagSearch'
import FileDropzone from '../components/FileDropzone'
import TopKInput from '../components/TopKInput'
import Button from '../components/Button'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import ResultList from '../components/ResultList'

const Page = styled.div`
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`

const Title = styled.h1`
  margin: 0;
  font-size: 1.75rem;
`

const Subtitle = styled.p`
  margin: 0;
  color: #666;
`

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`

const Row = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`

function ImageSearchPage() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [topK, setTopK] = useState(5)
  const fileInputRef = useRef(null)

  const { mutate, data, isPending, isError, error, reset } = useImageRagSearch()

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile)
    setPreviewUrl(selectedFile ? URL.createObjectURL(selectedFile) : null)
    reset()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!file) return
    mutate({ file, topK })
  }

  return (
    <Page>
      <div>
        <Title>음식 사진으로 비슷한 메뉴 찾기</Title>
        <Subtitle>사진을 업로드하면 유사한 음식 이미지를 찾아드려요.</Subtitle>
      </div>

      <Form onSubmit={handleSubmit}>
        <FileDropzone ref={fileInputRef} previewUrl={previewUrl} onFileSelect={handleFileSelect} />

        <Row>
          <TopKInput value={topK} onChange={setTopK} />
          <Button type="submit" disabled={!file || isPending}>
            {isPending ? '검색 중...' : '검색하기'}
          </Button>
        </Row>
      </Form>

      {isPending && <LoadingSpinner />}
      {isError && <ErrorMessage message={error.message} />}
      {data && <ResultList queryCaption={data.query_caption} results={data.results} />}
    </Page>
  )
}

export default ImageSearchPage
