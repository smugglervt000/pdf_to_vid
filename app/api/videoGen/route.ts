import { NextRequest, NextResponse } from "next/server";
import { promises as fs } from "fs";
import { v4 as uuidv4 } from "uuid";
import { exec } from "child_process";
import path from "path";

export async function POST(req: Request) {
	let targetPath = "";

	if (process.env.DOCKER) {
		targetPath = path.join(__dirname, "../../../../../../app");
	} else {
		console.log("not docker");
		targetPath = path.join(__dirname, "../../../../../api");
	}

    const { scriptValue, musicValue } = await req.json();
    // save scriptvalue to txt
    const scriptjson = JSON.stringify({ scriptValue });
	console.log("musicValue", musicValue);

    //save to file
    const tempFilePath = `${targetPath}/outputs/readyScript.txt`;
    await fs
        .writeFile(tempFilePath, scriptValue)
        .then(() => console.log("File written successfully"))
        .catch((err) => console.log("Error writing to file:", err));
    const subPath = path.join(targetPath, "subtitles_imageprompts.py");

	console.log("subtitles");

	const subtitle = await new Promise((resolve, reject) => {
		exec(`python3 ${subPath}`, (error, stdout, stderr) => {
			if (error) {
				console.error(`exec error: ${error}`);
				reject(`Error parsing PDF: ${error}`);
			}

			resolve(stdout); // Resolve the promise with the parsed text
		});
	});
console.log("subtitles done");

	console.log("video generation");

	const vidPath = path.join(targetPath, "/video_generation_helper.py");

	const video = await new Promise((resolve, reject) => {
		exec(`python3 ${vidPath} `, (error, stdout, stderr) => {
			if (error) {
				console.error(`exec error: ${error}`);
				reject(`Error parsing PDF: ${error}`);
			}

			resolve(stdout); // Resolve the promise with the parsed text
		});
	});
}