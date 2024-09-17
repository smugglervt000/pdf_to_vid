import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
	return [
		{
			url: "https://demo.useAI PDF to Video?.com",
			lastModified: new Date(),
		},
		{
			url: "https://demo.useAI PDF to Video?.com/demo",
			lastModified: new Date(),
		},
	];
}