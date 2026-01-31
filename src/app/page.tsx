import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Image
          className={styles.projectLogo}
          src="/logo.png"
          alt="Salmon Race Logo"
          width={227}
          height={157}
          priority
        />
        <div className={styles.riverContainer}>
          <div className={styles.lanes}>
            <div className={styles.lane} />
            <div className={styles.lane} />
            <div className={styles.lane} />
            <div className={styles.lane} />
            <div className={styles.lane} />
            <div className={styles.lane} />
          </div>
        </div>
      </main>
    </div>
  );
}
