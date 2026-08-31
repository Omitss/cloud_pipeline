import styled from 'styled-components'

const Box = styled.p`
  margin: 0;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 0.9rem;
`

function ErrorMessage({ message }) {
  return <Box role="alert">{message}</Box>
}

export default ErrorMessage
