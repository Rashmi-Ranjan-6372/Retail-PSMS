import { Flex, Box } from "@chakra-ui/react";

import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

import {
  layoutWrapper,
  sidebarWrapper,
  contentWrapper,
  navbarWrapper,
  pageWrapper,
  pageContent,
} from "../../../styles/components/layout";

import {
  pageBackground,
  blobOne,
  blobTwo,
} from "../../../styles/common/background";

const Layout = ({ children }) => {
  return (
    <Flex sx={layoutWrapper}>
      <Box sx={sidebarWrapper}>
        <Sidebar />
      </Box>

      <Flex sx={contentWrapper}>
        <Box sx={navbarWrapper}>
          <Navbar />
        </Box>

        <Box sx={pageWrapper}>
          <Box sx={pageBackground}>
            <Box sx={blobOne} />
            <Box sx={blobTwo} />
          </Box>

          <Box sx={pageContent}>{children}</Box>
        </Box>
      </Flex>
    </Flex>
  );
};

export default Layout;
