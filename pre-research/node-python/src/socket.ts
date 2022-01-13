import { Server } from "socket.io";
import express from "express";
import http from "http";

function socket(server: http.Server, app: express.Application) {
  const io = new Server(server, {
    path: "/socket.io",
    cors: {
      origin: "http://localhost:3000",
      credentials: true,
    },
  });

  app.set("io", io);

  io.on("connection", (socket) => {
    console.log("[socket.io] connection :)");

    socket.on("disconnect", () => {
      console.log("[socket.io] disconnection :)");
    });
  });
}
export default socket;
