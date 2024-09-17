import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import { v4 as uuidv4 } from 'uuid';
import { exec } from 'child_process';
import path from 'path';

export async function POST(req: Request) {
    let targetPath = '';

    if (process.env.DOCKER) {
        targetPath = path.join(__dirname, '../../../../../../app');
    } else {
        console.log('not docker');
        targetPath = path.join(__dirname, '../../../../../api');
    }

    const { selectedTopics, selectedStyle, selectedLength, selectedMusic, selectedVoice } = await req.json();
    // save to json
    const topicjson = JSON.stringify({ selectedTopics, selectedStyle, selectedLength, selectedMusic, selectedVoice });
    //save to file
         const tempFilePath = `${targetPath}/outputs/selected.json`;
    await fs
        .writeFile(tempFilePath, topicjson)
        .then(() => console.log('File written successfully'))
        .catch((err) => console.log('Error writing to file:', err));

    
         
    const sumPath = path.join(targetPath, 'script_generation.py');
    console.log('script generation');
    const summary = await new Promise((resolve, reject) => {
      exec(`python3 ${sumPath}`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          reject(`Error parsing PDF: ${error}`);
        }

        resolve(stdout); // Resolve the promise with the parsed text
      });
    });
    //   load from script.txt
    const script = await fs.readFile
    (path.join(targetPath, '/outputs/script.txt'), 'utf8');
    console.log(script);
 
    // Assuming you're sending back the parsed text as the response
    return new NextResponse(JSON.stringify({script,  }), {
      headers: {
          'Content-Type': 'text/plain', // Ensure you set an appropriate content type
      },
    });

    } 