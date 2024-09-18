'use client';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import { useState } from 'react';

interface UploaderProps {
  onServerId: (serverId: string) => void;
}

const Uploader: React.FC<UploaderProps> = ({ onServerId }) => {
  const [files, setFiles] = useState([]);

  const handleProcessFile = (error: any, file: any) => {
    console.log("id", file.id);
    if (onServerId) {
      onServerId(file.serverId); // Call the callback with the server ID
    }
  };

  return (
    <FilePond
      files={files}
      allowMultiple={true}
      onprocessfile={handleProcessFile}
      server={{
        process: '/api/upload',
        fetch: null,
        revert: null,
        
      }}
    />
  );
} 

export default Uploader;