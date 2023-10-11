import React, { useState } from "react";


const LoginForm = () => {

  const [userName, setuserName] = useState("");
  const [password, setPassword] = useState("");
//   const [message, setMessage] = useState("");

  
  const handleLogin = async (e) => {
    e.preventDefault();
  
    const response = await fetch('/login', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userName, password }),
    });
  
    const data = await response.json();
    
    console.log("Response data:", data.role);
  
   
  };
  


  return (
    <div className="form1">
      <h1 style={{color:'white', paddingTop:'30px'}}>Login</h1>
      {/* {message && <p>{message}</p>} */}
      <form className="signup" onSubmit={handleLogin} style={{color:'white'}} >
        <div>
          <label>User Name:</label>
          <input type="text" value={userName} onChange={(e) => setuserName(e.target.value)} />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div>
  
</div>

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
