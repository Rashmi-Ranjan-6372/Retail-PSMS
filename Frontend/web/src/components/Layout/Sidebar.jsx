import React, { useMemo, useState, useEffect } from "react";
import {
  Box,
  Flex,
  Icon,
  Text,
  VStack,
  Collapse,
  Image,
  useColorModeValue,
} from "@chakra-ui/react";

import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { useNavigate, useLocation } from "react-router-dom";

import { getSidebarByRole } from "../../config/navigation";
import useAuth from "../../hooks/useAuth";
import DefaultLogo from "../../assets/pharmacy-icons/pharmacy-logo.svg";

import "../../styles/Layout/sidebar.css";

/* ===================================================
   HELPER FUNCTIONS
=================================================== */

const hasActiveChild = (menu, pathname) => {
  if (!menu.children) return false;

  return menu.children.some(
    (child) =>
      child.path === pathname ||
      (child.children && hasActiveChild(child, pathname))
  );
};

const isMenuActive = (menu, pathname) => {
  return (
    menu.path === pathname ||
    (menu.children && hasActiveChild(menu, pathname))
  );
};

const getDefaultOpenMenus = (menus, pathname) => {
  let opened = [];

  menus.forEach((menu) => {
    if (menu.children) {
      if (hasActiveChild(menu, pathname)) {
        opened.push(menu.id);
      }

      opened = [
        ...opened,
        ...getDefaultOpenMenus(menu.children, pathname),
      ];
    }
  });

  return opened;
};

/* ===================================================
   MENU ITEM
=================================================== */

const MenuItem = ({
  item,
  level,
  pathname,
  navigate,
  openedMenus,
  setOpenedMenus,
}) => {
  const hasChildren = item.children?.length > 0;

  const isOpen = openedMenus.includes(item.id);

  const isActive = isMenuActive(item, pathname);

  const textColor = useColorModeValue("gray.700", "gray.100");

  const toggleMenu = () => {
    if (!hasChildren) return;

    if (isOpen) {
      setOpenedMenus([]);
    } else {
      setOpenedMenus([item.id]);
    }
  };

  return (
    <Box>
      <Flex
        className={`sidebar-item ${isActive ? "active" : ""}`}
        align="center"
        justify="space-between"
        pl={`${level * 20 + 14}px`}
        pr="14px"
        py="13px"
        color={isActive ? "white" : textColor}
        onClick={() => {
          if (hasChildren) {
            toggleMenu();
          } else {
            navigate(item.path);
          }
        }}
      >
        <Flex align="center" gap={3}>
          {item.icon && (
            <Icon
              as={item.icon}
              boxSize={5}
              className="sidebar-icon"
              color={isActive ? "white" : "blue.500"}
            />
          )}

          <Text
            fontSize="14px"
            fontWeight="600"
            letterSpacing=".2px"
          >
            {item.label}
          </Text>
        </Flex>

        {hasChildren && (
          <Icon
            as={isOpen ? FaChevronUp : FaChevronDown}
            fontSize="12px"
            transition=".25s"
            transform={isOpen ? "rotate(180deg)" : "rotate(0deg)"}
          />
        )}
      </Flex>

      {hasChildren && (
        <Collapse in={isOpen} animateOpacity>
          <VStack
            align="stretch"
            spacing={1}
            mt={1}
          >
            {item.children.map((child, index) => (
              <MenuItem
                key={
                  child.id ??
                  child.path ??
                  `${item.id}-${index}`
                }
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

/* ===================================================
   SIDEBAR COMPONENT
=================================================== */

const Sidebar = () => {
  const { role, user } = useAuth();

  const navigate = useNavigate();
  const { pathname } = useLocation();

  const sidebarMenus = useMemo(() => {
    if (!role) return [];
    return getSidebarByRole(role);
  }, [role]);

  const defaultOpened = useMemo(
    () => getDefaultOpenMenus(sidebarMenus, pathname),
    [sidebarMenus, pathname]
  );

  const [openedMenus, setOpenedMenus] = useState(defaultOpened);

  useEffect(() => {
    setOpenedMenus(defaultOpened);
  }, [defaultOpened]);

  const logoSrc =
    user?.company_logo ||
    user?.logo ||
    user?.organization?.logo ||
    DefaultLogo;

  return (
    <Box className="sidebar">
      {/* =========================
          HEADER
      ========================= */}

      <Flex className="sidebar-header">
        <Box className="sidebar-logo">
          <Image
            src={logoSrc}
            alt="Company Logo"
            fallbackSrc={DefaultLogo}
          />
        </Box>
      </Flex>

      {/* =========================
          MENU
      ========================= */}

      <Box className="sidebar-menu">
        <VStack align="stretch" spacing={2}>
          {sidebarMenus.map((menu, index) => (
            <MenuItem
              key={menu.id ?? menu.path ?? `menu-${index}`}
              item={menu}
              level={0}
              pathname={pathname}
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