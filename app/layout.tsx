import "../styles/globals.css";
import { Metadata } from "next";

import { Providers } from "./providers";

export const metadata: Metadata = {
	title: "AI PDF to Video",
	openGraph: {
		title: "AI PDF to Video",
		description:
			"AI PDF to Video is a web application that converts your PDF files into videos.",
		images: [
			{
				url: "https://demo.useAI PDF to Video?.com/opengraph-image",
			},
		],
	},

	themeColor: "#FFF",
};
export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang="en" className="light">
			<body>
				<Providers>{children}</Providers>
			</body>
		</html>
	);
}