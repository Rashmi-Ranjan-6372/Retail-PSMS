import { Flex, Box } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

const Layout = ({ children }) => {
  return (
    <Flex>
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <Box flex="1">
        <Navbar />

        <Box p={5}>
          {children}
        </Box>
      </Box>
    </Flex>
  );
};

export default Layout;