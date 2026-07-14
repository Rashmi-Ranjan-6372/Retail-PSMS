import { useState } from "react";
import {
  Flex,
  Box,
  HStack,
  Input,
  InputGroup,
  InputLeftElement,
  IconButton,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Text,
  Select,
  Divider,
} from "@chakra-ui/react";

import { FaBell, FaSearch, FaUser, FaCog, FaSignOutAlt } from "react-icons/fa";

import useAuth from "../../../hooks/useAuth";

import navbar from "../../../styles/components/layout/navbar";
import { searchInput } from "../../../styles/components/inputs";
import { notificationButton } from "../../../styles/components/buttons";
import { notificationBadge } from "../../../styles/components/badges";

const Navbar = () => {
  const { user, logout } = useAuth();

  const [selectedBranch, setSelectedBranch] = useState("main");

  const isSuperAdmin = user?.role === "superadmin";

  return (
    <Flex sx={navbar.navbarWrapper}>
      {/* Search */}
      <Box sx={navbar.searchWrapper}>
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <FaSearch />
          </InputLeftElement>

          <Input
            sx={searchInput}
            placeholder="Search products, invoices, customers..."
          />
        </InputGroup>
      </Box>

      {/* Right Section */}
      <HStack spacing={4} sx={navbar.rightSection}>
        {/* Branch */}
        {isSuperAdmin && (
          <Box sx={navbar.branchWrapper}>
            <Select
              value={selectedBranch}
              onChange={(e) => setSelectedBranch(e.target.value)}
            >
              <option value="main">Main Branch</option>
              <option value="bbsr">Bhubaneswar</option>
              <option value="ctc">Cuttack</option>
              <option value="puri">Puri</option>
              <option value="berhampur">Berhampur</option>
            </Select>
          </Box>
        )}

        {/* Notification */}
        <Box sx={navbar.notificationWrapper}>
          <IconButton
            aria-label="Notifications"
            icon={<FaBell />}
            variant="ghost"
            sx={notificationButton}
          />

          <Box sx={notificationBadge}>5</Box>
        </Box>

        {/* User */}
        <Menu>
          <MenuButton>
            <HStack sx={navbar.userButton}>
              <Avatar
                size="sm"
                name={user?.name || "Admin"}
                src={user?.profile_image}
              />

              <Box sx={navbar.userInfo}>
                <Text sx={navbar.userName}>
                  {user?.name || "Administrator"}
                </Text>

                <Text sx={navbar.userRole}>{user?.role || "Super Admin"}</Text>
              </Box>
            </HStack>
          </MenuButton>

          <MenuList sx={navbar.menuList}>
            <Box sx={navbar.profileCard}>
              <Avatar
                size="md"
                name={user?.name || "Admin"}
                src={user?.profile_image}
                mx="auto"
                mb={3}
              />

              <Text sx={navbar.userName}>{user?.name || "Administrator"}</Text>

              <Text sx={navbar.userRole}>
                {user?.email || "admin@example.com"}
              </Text>
            </Box>

            <Divider sx={navbar.divider} />

            <MenuItem icon={<FaUser />} sx={navbar.menuItem}>
              Profile
            </MenuItem>

            <MenuItem icon={<FaCog />} sx={navbar.menuItem}>
              Settings
            </MenuItem>

            <Divider sx={navbar.divider} />

            <MenuItem
              icon={<FaSignOutAlt />}
              sx={navbar.logoutItem}
              onClick={logout}
            >
              Logout
            </MenuItem>
          </MenuList>
        </Menu>
      </HStack>
    </Flex>
  );
};

export default Navbar;
