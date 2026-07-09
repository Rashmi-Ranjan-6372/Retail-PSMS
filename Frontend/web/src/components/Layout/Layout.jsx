import { Flex, Box } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import { colors } from "../../styles/common/colors";
import backgrounds from "../../styles/common/background";

const Layout = ({ children }) => {
  return (
    <Flex h="100vh" overflow="hidden">
      {/* Sidebar */}
      <Box flexShrink={0}>
        <Sidebar />
      </Box>

      {/* Right Side */}
      <Flex flex="1" direction="column" overflow="hidden">
        {/* Navbar */}
        <Box flexShrink={0} zIndex={10}>
          <Navbar />
        </Box>

        {/* Content Area */}
        <Box
          flex="1"
          position="relative"
          overflow="hidden"
          bg={colors.background}
        >
          {/* Animated Background */}
          <Box sx={backgrounds.pageBackground}>
            <Box sx={backgrounds.blobOne} />
            <Box sx={backgrounds.blobTwo} />
          </Box>

          {/* All Pages */}
          <Box
            position="relative"
            zIndex={2}
            h="100%"
            overflowY="auto"
            px={6}
            py={6}
          >
            {children}
          </Box>
        </Box>
      </Flex>
    </Flex>
  );
};

export default Layout;
