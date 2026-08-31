import { forwardRef, useCallback, useState } from 'react'
import styled from 'styled-components'

const Zone = styled.label`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 220px;
  border: 2px dashed ${(p) => (p.$isDragging ? '#4f46e5' : '#cbd5e1')};
  border-radius: 12px;
  background: ${(p) => (p.$isDragging ? '#eef2ff' : '#f8fafc')};
  color: #64748b;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.15s ease, background 0.15s ease;
`

const HiddenInput = styled.input`
  display: none;
`

const Preview = styled.img`
  max-width: 100%;
  max-height: 260px;
  border-radius: 8px;
  object-fit: contain;
`

const Hint = styled.span`
  font-size: 0.9rem;
`

const FileDropzone = forwardRef(function FileDropzone({ previewUrl, onFileSelect }, ref) {
  const [isDragging, setIsDragging] = useState(false)

  const handleFiles = useCallback(
    (fileList) => {
      const selected = fileList?.[0]
      if (selected) onFileSelect(selected)
    },
    [onFileSelect],
  )

  return (
    <Zone
      $isDragging={isDragging}
      onDragOver={(e) => {
        e.preventDefault()
        setIsDragging(true)
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault()
        setIsDragging(false)
        handleFiles(e.dataTransfer.files)
      }}
    >
      {previewUrl ? (
        <Preview src={previewUrl} alt="선택된 이미지 미리보기" />
      ) : (
        <Hint>이미지를 드래그하거나 클릭해서 선택하세요</Hint>
      )}
      <HiddenInput
        ref={ref}
        type="file"
        accept="image/*"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </Zone>
  )
})

export default FileDropzone
