import childProcess from "child_process";

const spawn = childProcess.spawn;
const result = spawn("python3", ["python/index.py"]);

result.stdout.on("data", (data: any) => {
  console.log(data.toString());
});
