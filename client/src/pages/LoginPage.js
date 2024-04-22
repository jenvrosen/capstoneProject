import React from "react";
import LoginForm from "../components/LoginForm";
import BaseLayout from "../components/BaseLayout";

const LoginPage = () => {
  return (
    <BaseLayout hideNavigation={true}>
      <LoginForm />
    </BaseLayout>
  );
};

export default LoginPage;
