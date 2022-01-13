import childProcess from "child_process";

const spawn = childProcess.spawn;

const result = spawn("python3", ["python/index.py"]);
const result_argv = spawn("python3", ["python/index.py", "formegusto", "27"]);

result.stdout.on("data", (data: any) => {
  console.log("파이썬 실행완료");
  console.log(data.toString());
});

result_argv.stdout.on("data", (data: any) => {
  console.log("파이썬(argv) 실행완료");
  console.log(data.toString());
});
