// const sqli1_user_in = document.getElementById("sqli1_form_username");
// const sqli1_user_out = document.getElementById("sqli1_query_username");
// sqli1_user_in.addEventListener("input", (e) => {
//   sqli1_user_out.textContent = sqli1_user_in.textContent;
// });

// const sqli1_pass_in = document.getElementById("sqli1_form_password");
// const sqli1_pass_out = document.getElementById("sqli1_query_password");
// sqli1_pass_in.addEventListener("input", (e) => {
//   sqli1_pass_out.textContent = sqli1_pass_in.textContent;
// });

/* -------------------- */

// Mirrors the contents of the form input in_id to the element out_id.
// function mirror(in_id, out_id) {
//   console.log(in_id, out_id);
//   document.getElementById(out_id).textContent = document.getElementById(in_id).value;
//   hljs.highlightAll();
// }

/* Stage-specific functions */

function sqli1() {
  const username = document.getElementById('sqli1_form_username').value;
  const password = document.getElementById('sqli1_form_password').value;

  document.getElementById('sqli1_query').textContent = `SELECT username FROM Users WHERE username='${username}' AND password='${password}'`;

  hljs.highlightAll();
}