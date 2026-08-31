import styled from 'styled-components'
import { getResultImageUrl } from '../api/imageRagApi'

const Card = styled.li`
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #fff;
`

const Thumb = styled.img`
  width: 96px;
  height: 96px;
  flex-shrink: 0;
  border-radius: 8px;
  object-fit: cover;
`

const Info = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`

const DishName = styled.h3`
  margin: 0;
  font-size: 1.05rem;
`

const Similarity = styled.span`
  font-size: 0.85rem;
  font-weight: 600;
  color: #4f46e5;
`

const Caption = styled.p`
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
`

function ResultCard({ result }) {
  const { dish_name, image_path, similarity, caption } = result

  return (
    <Card>
      <Thumb src={getResultImageUrl(dish_name, image_path)} alt={dish_name} loading="lazy" />
      <Info>
        <DishName>{dish_name}</DishName>
        <Similarity>유사도 {Math.round(similarity * 100)}%</Similarity>
        <Caption>{caption}</Caption>
      </Info>
    </Card>
  )
}

export default ResultCard
