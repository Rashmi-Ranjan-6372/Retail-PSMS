import { Flex, Box } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import { colors } from "../../styles/common/colors";

const Layout = ({ children }) => {
  return (
    <Flex h="100vh" overflow="hidden">
      {/* Sidebar */}
      <Box>
        <Sidebar />
      </Box>

      {/* Right Side */}
      <Flex flex="1" direction="column" overflow="hidden">
        {/* Navbar */}
        <Box flexShrink={0}>
          <Navbar />
        </Box>

        {/* Scrollable Content */}
        <Box flex="1" overflowY="auto" bg={colors.backgroundLight}>
          {children}
      </Box>
      </Flex>
    </Flex>
  );
};

export default Layout;
