import React from "react";
import { useSelector } from "react-redux";

// components for this page
import Nav from "../components/Index/Nav";
import Table from "../components/Index/Table";
import AdminDialog from "../components/Index/AdminDialog";
import BookingDialog from "../components/Index/BookingDialog";

function Index() {
  // redux
  const user = useSelector((state) => state.user);

  return (
    <div>
      <Nav />
      {user.is_admin && <AdminDialog />}
      <BookingDialog />
      <Table />
    </div>
  );
}

export default Index;
