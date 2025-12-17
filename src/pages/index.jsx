import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/part0-introduction">
            Start Learning
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="The Official Panaversity AI-Native Textbook for Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <div className="container margin-vert--xl">
          <div className="row">
            <div className="col col--4">
              <div className="text--center padding-horiz--md">
                <h3>Comprehensive Learning</h3>
                <p>
                  From fundamentals to advanced topics in humanoid robotics and physical AI systems.
                </p>
              </div>
            </div>
            <div className="col col--4">
              <div className="text--center padding-horiz--md">
                <h3>AI-Powered Assistant</h3>
                <p>
                  Get instant help with our integrated RAG chatbot powered by OpenAI ChatKit.
                </p>
              </div>
            </div>
            <div className="col col--4">
              <div className="text--center padding-horiz--md">
                <h3>Interactive Content</h3>
                <p>
                  Engage with interactive examples, diagrams, and real-world applications.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
