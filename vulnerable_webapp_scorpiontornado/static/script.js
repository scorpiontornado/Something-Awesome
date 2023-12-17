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

  const sqli1_query = document.getElementById('sqli1_query');
  sqli1_query.textContent = `SELECT username FROM Users WHERE username='${username}' AND password='${password}'`;
  sqli1_query.removeAttribute('data-highlighted');

  hljs.highlightAll();
} 

function sqli2() {
  const student_id = document.getElementById('sqli2_student_id').value;

  const sqli2_query = document.getElementById('sqli2_query');
  sqli2_query.textContent = `SELECT first_name, last_name, email FROM Students WHERE student_id = ${student_id}`;
  sqli2_query.removeAttribute('data-highlighted');

  hljs.highlightAll();
}

// Could combine with sqli2 but not really worth it
function sqli3() {
  const student_id = document.getElementById('sqli3_student_id').value;

  // TODO find and replace

  const sqli3_query = document.getElementById('sqli3_query');
  sqli3_query.textContent = `SELECT first_name, last_name, email FROM Students WHERE student_id = ${student_id}`;
  sqli3_query.removeAttribute('data-highlighted');

  hljs.highlightAll();
}