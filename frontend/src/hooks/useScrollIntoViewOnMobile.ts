import { useEffect, type RefObject } from "react";

import { MOBILE_MEDIA_QUERY } from "../config/layout";

export function useScrollIntoViewOnMobile(
  ref: RefObject<HTMLElement | null>,
  shouldScroll: boolean
) {
  useEffect(() => {
    if (!shouldScroll) return;

    if (window.matchMedia(MOBILE_MEDIA_QUERY).matches) {
      ref.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [ref, shouldScroll]);
}