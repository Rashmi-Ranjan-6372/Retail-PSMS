import React, { useMemo, useState, useEffect } from "react";
import {
  Box,
  Flex,
  Icon,
  Text,
  VStack,
  Collapse,
  Image,
} from "@chakra-ui/react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { useNavigate, useLocation } from "react-router-dom";

import useAuth from "../../../hooks/useAuth";
import { getSidebarByRole } from "../../../config/navigation";

import DefaultLogo from "../../../assets/pharmacy-icons/pharmacy-logo.svg";

import sidebar from "../../../styles/components/layout/sidebar";
import { colors } from "../../../styles/common/colors";

const hasActiveChild = (menu, pathname) => {
  if (!menu.children) return false;

  return menu.children.some((child) => {
    if (child.path) return pathname === child.path;
    return child.children && hasActiveChild(child, pathname);
  });
};

const isMenuActive = (menu, pathname) => {
  if (menu.path) return pathname === menu.path;
  return hasActiveChild(menu, pathname);
};

const getDefaultOpenMenus = (menus, pathname) => {
  let opened = [];

  menus.forEach((menu) => {
    if (menu.children) {
      if (hasActiveChild(menu, pathname)) {
        opened.push(menu.id);
      }

      opened = [...opened, ...getDefaultOpenMenus(menu.children, pathname)];
    }
  });

  return opened;
};

const MenuItem = ({
  item,
  level = 0,
  pathname,
  navigate,
  openedMenus,
  setOpenedMenus,
}) => {
  const hasChildren = item.children?.length > 0;

  const isOpen = openedMenus.includes(item.id);

  const isActive = isMenuActive(item, pathname);

  const handleClick = () => {
    if (hasChildren) {
      setOpenedMenus((prev) =>
        isOpen ? prev.filter((id) => id !== item.id) : [...prev, item.id],
      );
    } else if (item.path) {
      navigate(item.path);
    }
  };

  return (
    <Box>
      <Flex
        sx={{
          ...sidebar.sidebarItem,
          ...(isActive ? sidebar.sidebarActive : sidebar.sidebarInactive),
          pl: `${level === 0 ? 18 : level * 20 + 18}px`,
        }}
        onClick={handleClick}
      >
        <Flex sx={sidebar.sidebarItemContent}>
          {item.icon && (
            <Icon
              as={item.icon}
              sx={{
                ...sidebar.sidebarIcon,
                color: isActive ? colors.white : colors.primary,
              }}
            />
          )}

          <Text
            sx={{
              ...sidebar.sidebarItemText,
              color: isActive ? colors.white : colors.textPrimary,
            }}
          >
            {item.label}
          </Text>
        </Flex>

        {hasChildren && (
          <Icon
            as={isOpen ? FaChevronUp : FaChevronDown}
            sx={{
              ...sidebar.sidebarChevron,
              color: isActive ? colors.white : colors.textSecondary,
            }}
          />
        )}
      </Flex>

      {hasChildren && (
        <Collapse in={isOpen} animateOpacity>
          <VStack align="stretch" spacing={1} sx={sidebar.sidebarSubMenu}>
            {item.children.map((child, index) => (
              <MenuItem
                key={child.id || child.path || index}
                item={child}
                level={level + 1}
                pathname={pathname}
                navigate={navigate}
                openedMenus={openedMenus}
                setOpenedMenus={setOpenedMenus}
              />
            ))}
          </VStack>
        </Collapse>
      )}
    </Box>
  );
};

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { role, user } = useAuth();

  const sidebarMenus = useMemo(() => {
    if (!role) return [];
    return getSidebarByRole(role);
  }, [role]);

  const defaultOpenedMenus = useMemo(
    () => getDefaultOpenMenus(sidebarMenus, location.pathname),
    [sidebarMenus, location.pathname],
  );

  const [openedMenus, setOpenedMenus] = useState(defaultOpenedMenus);

  useEffect(() => {
    setOpenedMenus(defaultOpenedMenus);
  }, [defaultOpenedMenus]);

  const logo =
    user?.company_logo || user?.logo || user?.organization?.logo || DefaultLogo;

  return (
    <Box sx={sidebar.sidebarWrapper}>
      <Flex sx={sidebar.sidebarHeader}>
        <Box sx={sidebar.sidebarLogoWrapper}>
          <Image
            src={logo}
            alt="Company Logo"
            fallbackSrc={DefaultLogo}
            sx={sidebar.sidebarLogoImage}
          />
        </Box>
      </Flex>

      <Box sx={sidebar.sidebarMenuWrapper}>
        <VStack align="stretch" spacing={2} sx={sidebar.sidebarMenu}>
          {sidebarMenus.map((menu, index) => (
            <MenuItem
              key={menu.id || menu.path || index}
              item={menu}
              pathname={location.pathname}
              navigate={navigate}
              openedMenus={openedMenus}
              setOpenedMenus={setOpenedMenus}
            />
          ))}
        </VStack>
      </Box>
    </Box>
  );
};

export default Sidebar;
