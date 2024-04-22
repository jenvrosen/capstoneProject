import React from "react";
import SignupForm from "../components/SignupForm";
import BaseLayout from "../components/BaseLayout";

const SignupPage = () => {
  return (
    <BaseLayout hideNavigation={true}>
      <SignupForm />
    </BaseLayout>
  );
};

export default SignupPage;
