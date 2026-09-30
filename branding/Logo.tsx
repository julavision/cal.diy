import classNames from "@calcom/ui/classNames";

// VisionCal — replaces packages/ui/components/logo/Logo.tsx at build time
// (branding/apply.sh). Cal.diy shows ONE logo and flips it with `dark:invert`
// in dark mode, which would turn the red "CAL" teal. Instead: the dark-text
// logo on light backgrounds, the light-text logo on dark ones.
const NAME = "VisionCal";
const DEFAULT_SRC = "/api/logo";

export function Logo({
  small,
  icon,
  inline = true,
  className,
  src = DEFAULT_SRC,
}: {
  small?: boolean;
  icon?: boolean;
  inline?: boolean;
  className?: string;
  src?: string;
}) {
  // A caller passing its own src (a team or org logo) gets exactly that, uninverted.
  const ours = src === DEFAULT_SRC;
  const size = small ? "h-4 w-auto" : "h-5 w-auto";
  return (
    <h3 className={classNames("logo", inline && "inline", className)}>
      <strong>
        {icon ? (
          <>
            <img className={classNames("mx-auto w-9", ours && "dark:hidden")} alt={NAME} title={NAME} src={`${src}?type=icon`} />
            {ours && <img className="mx-auto hidden w-9 dark:block" alt={NAME} title={NAME} src="/cal-com-icon.svg" />}
          </>
        ) : (
          <>
            <img className={classNames(size, ours && "dark:hidden")} alt={NAME} title={NAME} src={src} />
            {ours && <img className={classNames(size, "hidden dark:inline")} alt={NAME} title={NAME} src="/cal-logo-word-dark.svg" />}
          </>
        )}
      </strong>
    </h3>
  );
}
