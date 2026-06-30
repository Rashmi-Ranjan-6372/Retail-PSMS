import { Flex, Box } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

const Layout = ({ children }) => {
  return (
    <Flex minH="100vh" bg="gray.50" gap={3}>
      {/* Sidebar */}
      <Box w="260px" bg="white">
        <Sidebar />
      </Box>

      {/* Main Content */}
      <Box flex="1" display="flex" flexDirection="column">
        {/* Navbar */}
        <Box position="sticky" top="0" zIndex="10" bg="white">
          <Navbar />
        </Box>

        {/* Page Content */}
        <Box flex="1" p={5} bg="gray.50">
          {children}
        </Box>
      </Box>
    </Flex>
  );
};

export default Layout;
