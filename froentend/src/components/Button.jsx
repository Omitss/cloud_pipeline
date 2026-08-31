import styled from 'styled-components'

const Button = styled.button`
  padding: 0.6rem 1.4rem;
  border: none;
  border-radius: 8px;
  background: #4f46e5;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;

  &:hover:not(:disabled) {
    background: #4338ca;
  }

  &:disabled {
    background: #c7d2fe;
    cursor: not-allowed;
  }
`

export default Button
