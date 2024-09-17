import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import { v4 as uuidv4 } from 'uuid';
import { exec } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest) {
  const formData: FormData = await req.formData();
  const uploadedFiles = formData.getAll('filepond');
  let fileName = '';

  if (uploadedFiles && uploadedFiles.length > 0) {
    const uploadedFile = uploadedFiles[1] as File; 
    console.log('Uploaded file:', uploadedFile.name);

    if (uploadedFile instanceof File) {
      let ifDocker = false;
      if (process.env.DOCKER) {
        ifDocker = true;
      }
      fileName = uuidv4();
      const tempFilePath = `/tmp/${fileName}.pdf`;
      const fileBuffer = Buffer.from(await uploadedFile.arrayBuffer());
      await fs.writeFile(tempFilePath, fileBuffer);

      // Get path to python file
    
      let targetPath = '';
      if (process.env.DOCKER) {
        targetPath = path.join(__dirname, '../../../../../../app');
      } else {
        console.log('not docker');
        targetPath = path.join(__dirname, '../../../../../api');
      }
      const scriptPath = path.join(targetPath, 'pdf_parser.py');
      console.log('parsing', scriptPath, tempFilePath);
      // Use a promise to wait for the exec to complete
      const tempText = await new Promise((resolve, reject) => {
        exec(`python3 "${scriptPath}" "${tempFilePath}"`, (error, stdout, stderr) => {
          if (error) {
            console.error(`exec error: ${error}`);
            reject(`Error parsing PDF: ${error}`);
          }

          resolve(stdout); // Resolve the promise with the parsed text
        });
      });
      console.log('topicextraction');
      const topicPath = path.join(targetPath, 'topic_extraction.py');
      // console.log(`python3 "${topicPath}"   "${parsedText}`)
      const topicextraction = await new Promise((resolve, reject) => {
        exec(`python3 ${topicPath}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`exec error: ${error}`);
            reject(`Error parsing PDF: ${error}`);
          }

          resolve(stdout); // Resolve the promise with the parsed text
        });
      });

      // load topic.json
      const topicjson = await fs.readFile
      (path.join(targetPath, '/outputs/topic.json'), 'utf8');
      console.log("this is topicjson", topicjson);
      // load parse.txt
      const parsedText = await fs.readFile
      (path.join(targetPath, '/outputs/parse.txt'), 'utf8');
      console.log(parsedText);

      // Assuming you're sending back the parsed text as the response
      return new NextResponse(JSON.stringify({parsedText, topicjson,  }), {
        headers: {
          'FileName': fileName,
          'Content-Type': 'text/plain', // Ensure you set an appropriate content type
          
        },
      });

    } else {
      console.log('Uploaded file is not in the expected format.');
      return new NextResponse('Uploaded file is not in the expected format.', { status: 400 });
    }
  } else {
    console.log('No files found.');
    return new NextResponse('No files found.', { status: 400 });
  }

  



}