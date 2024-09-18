/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
  
    reactStrictMode: false,
    experimental: {
      serverComponentsExternalPackages: ['pdf2json'],
    },
  
    async headers() {
      return [
        {
          source: "/(.*)",
          headers: [
            {
              key: "Cross-Origin-Embedder-Policy",
              value: "require-corp",
            },
            {
              key: "Cross-Origin-Opener-Policy",
              value: "same-origin",
            },
          ],
        },
      ];
    },
  };
  
  module.exports = nextConfig;