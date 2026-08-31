import styled from 'styled-components'
import ResultCard from './ResultCard'

const Section = styled.section`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`

const QueryCaption = styled.p`
  margin: 0;
  font-size: 0.9rem;
  color: #475569;

  strong {
    color: #1e293b;
  }
`

const List = styled.ul`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 0;
  padding: 0;
  list-style: none;
`

const Empty = styled.p`
  margin: 0;
  color: #94a3b8;
`

function ResultList({ queryCaption, results }) {
  return (
    <Section>
      <QueryCaption>
        <strong>업로드 이미지 설명: </strong>
        {queryCaption}
      </QueryCaption>
      {results.length === 0 ? (
        <Empty>유사한 이미지를 찾지 못했어요.</Empty>
      ) : (
        <List>
          {results.map((result) => (
            <ResultCard key={result.image_path} result={result} />
          ))}
        </List>
      )}
    </Section>
  )
}

export default ResultList
