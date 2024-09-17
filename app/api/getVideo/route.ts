// app/api/getVideo/route.ts
import { NextResponse } from "next/server";
import path from "path";
import fs from "fs";

export async function GET() {
	let targetPath = "";

	if (process.env.DOCKER) {
		targetPath = path.join(
			__dirname,
			"../../../../../../app/public/finalready.mp4"
		);
	} else {
		console.log("not docker");
		targetPath =  path.join(__dirname, "../../../../../public/finalready.mp4");
		console.log("targetPath", targetPath);
	}

	try {
		const videoBuffer = await fs.promises.readFile(targetPath);
		return new NextResponse(videoBuffer, {
			status: 200,
			headers: {
				"Content-Type": "video/mp4",
			},
		});
	} catch (error) {
		 return new NextResponse(null, {
			status: 500,
			headers: {
				"Content-Type": "application/json",
			},
		});
	}
}