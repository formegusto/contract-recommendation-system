import express from "express";
import SSE from "sse";

export default function sse(server: express.Application) {
  const sse = new SSE(server);

  sse.on("connection", (client: any) => {
    console.log("Connection :)");
  });
}
