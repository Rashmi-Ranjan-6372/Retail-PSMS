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
  Badge,
} from "@chakra-ui/react";
import { FaBell, FaSearch, FaUser, FaCog, FaSignOutAlt } from "react-icons/fa";

import useAuth from "../../../hooks/useAuth";
import navbar from "../../styles/components/navbar";
import notificationBadge from "../../styles/common/badges";

const Navbar = () => {
  const { logout, user } = useAuth();

  const [selectedBranch, setSelectedBranch] = useState("main");

  const isSuperAdmin = user?.role === "superadmin";

  return (
    <Flex sx={navbar.navbarWrapper}>
      <Box sx={navbar.searchWrapper}>
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <FaSearch style={navbar.searchIcon} />
          </InputLeftElement>

          <Input
            sx={navbar.searchInput}
            placeholder="Search products, invoices, customers..."
          />
        </InputGroup>
      </Box>

      <HStack sx={navbar.rightSection}>
        {isSuperAdmin && (
          <Box sx={navbar.branchWrapper}>
            <Select
              sx={navbar.branchSelect}
              value={selectedBranch}
              onChange={(e) => setSelectedBranch(e.target.value)}
            >
              <option value="main">Main Branch</option>
              <option value="bbsr">Bhubaneswar Branch</option>
              <option value="ctc">Cuttack Branch</option>
              <option value="puri">Puri Branch</option>
              <option value="berhampur">Berhampur Branch</option>
            </Select>
          </Box>
        )}

        <Box sx={navbar.notificationWrapper}>
          <IconButton
            icon={<FaBell />}
            aria-label="Notifications"
            variant="ghost"
            sx={navbar.notificationButton}
          />

          <Badge sx={navbar.notificationBadge}>5</Badge>
        </Box>

        <Menu>
          <MenuButton>
            <HStack sx={navbar.userButton}>
              <Avatar
                size="sm"
                name={user?.name || "Admin"}
                src={user?.profile_image}
              />

              <Box sx={navbar.userInfo}>
                <Text sx={navbar.userName}>{user?.name || "Admin"}</Text>

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

              <Text sx={navbar.userName}>{user?.name || "Admin"}</Text>

              <Text sx={navbar.userRole}>
                {user?.email || "admin@example.com"}
              </Text>
            </Box>

            <MenuItem sx={navbar.menuItem} icon={<FaUser />}>
              Profile
            </MenuItem>

            <MenuItem sx={navbar.menuItem} icon={<FaCog />}>
              Settings
            </MenuItem>

            <MenuItem
              sx={navbar.logoutItem}
              icon={<FaSignOutAlt />}
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
