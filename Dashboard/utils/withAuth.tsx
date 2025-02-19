'use strict';
import { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';

const withAuth = <P extends object>(WrappedComponent: React.ComponentType<P>) => {
  const AuthComponent = (props: P) => {
    const [isClient, setIsClient] = useState(false);
    const router = useRouter();

    useEffect(() => {
      setIsClient(true); // Ensures we are on the client-side

      if (typeof window !== "undefined") {
        const accessToken = localStorage.getItem("accessToken");

        if (!accessToken) {
          router.push("/login");
        }
      }
    }, [router]);

    if (!isClient) return null; // Prevents SSR errors

    return <WrappedComponent {...props} />;
  };

  return AuthComponent;
};

export default withAuth;
