import { NextRequest, NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

export async function DELETE(request: NextRequest) {
	const filePath = path.join(process.cwd(), "public", "finalready.mp4");

	try {
		await fs.unlink(filePath);
		return NextResponse.json({ message: "Video deleted successfully" });
	} catch (error) {
		console.error("Error deleting video:", error);
		return NextResponse.json(
			{ message: "Error deleting video" },
			{ status: 500 }
		);
	}
}