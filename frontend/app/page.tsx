"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  async function handleAnalyze() {

    if (!file) {
      alert("Please select a Python file");
      return;
    }

    setLoading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append("file", file as File);

    try {

      const response = await axios.post(
        "https://ai-python-code-analyzer.onrender.com",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },

          onUploadProgress: (progressEvent) => {

            const percent = Math.round(
              (progressEvent.loaded * 100) /
              (progressEvent.total || 1)
            );

            setUploadProgress(percent);
          },
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);
      alert("Failed to connect to backend");

    } finally {

      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-5xl bg-white shadow-2xl rounded-3xl p-8">
        <h1 className="text-4xl font-bold mb-2">
          AI Python Code Analyzer
        </h1>

        <p className="text-gray-600 mb-8">
          Upload a Python file and analyze bugs, complexity,
          generated tests, and fix suggestions.
        </p>

        <div className="flex flex-col md:flex-row gap-4 items-center mt-8">
          <label className="flex items-center w-full border border-gray-300 rounded-2xl overflow-hidden bg-white shadow-sm">
    
            <span className="bg-gray-100 px-6 py-4 border-r border-gray-300 font-medium cursor-pointer hover:bg-gray-200 transition">
              Choose File
            </span>

            <span className="px-4 text-gray-500 truncate">
              {file ? file.name : "No file chosen"}
            </span>

            <input
              type="file"
              accept=".py"
              onChange={(e) => {
                if (e.target.files?.[0]) {
                  setFile(e.target.files[0]);
                }
              }}
              className="hidden"
            />
          </label>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-black text-white px-8 py-4 rounded-2xl hover:opacity-80 transition font-medium"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
        
        {loading && (

          <div className="mt-6">

            <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">

              <div
                className="bg-black h-4 transition-all duration-300"
                style={{
                  width: `${uploadProgress}%`,
                }}
              />

            </div>

            <p className="text-sm text-gray-600 mt-2">
              Uploading... {uploadProgress}%
            </p>

          </div>
        )}

        {result && (
          <div className="mt-10">
            <h2 className="text-2xl font-semibold mb-4">
              Analysis Results
            </h2>

            <div className="bg-black text-green-400 rounded-2xl p-6 overflow-auto max-h-[600px]">
              <pre className="text-sm whitespace-pre-wrap">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}