import styled from 'styled-components'

const Wrapper = styled.label`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #475569;
`

const NumberInput = styled.input`
  width: 60px;
  padding: 0.4rem 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
`

function TopKInput({ value, onChange }) {
  return (
    <Wrapper>
      결과 개수
      <NumberInput
        type="number"
        min={1}
        max={50}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </Wrapper>
  )
}

export default TopKInput
