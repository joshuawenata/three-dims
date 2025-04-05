"use client";
import { useState } from "react";

export default function Generator() {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [gifUrl, setGifUrl] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      setGifUrl(`http://localhost:8000/download/${data.id}`);
    } catch (error) {
      console.error("Generation error:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="bg-white w-screen h-screen flex items-center justify-center">
      <div className="container mx-auto p-6 md:p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          3D GIF Generator
        </h1>

        <form onSubmit={handleSubmit} className="mb-8 flex flex-col space-y-4">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your 3D object..."
            className="shadow appearance-none border rounded w-full py-3 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
          <button
            type="submit"
            disabled={isGenerating}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded focus:outline-none focus:shadow-outline disabled:bg-gray-400"
          >
            {isGenerating ? "Generating..." : "Generate GIF"}
          </button>
        </form>

        {gifUrl && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Preview
            </h2>
            <div className="shadow rounded overflow-hidden">
              <img src={gifUrl} alt="3D Preview" className="w-96 h-96" />
            </div>
            <a
              href={gifUrl}
              download="3d_model.gif"
              className="mt-4 inline-block bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Download GIF
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
