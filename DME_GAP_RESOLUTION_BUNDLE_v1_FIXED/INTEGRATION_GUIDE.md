# Integration Guide – DME Gap Resolution Bundle v1

1. Unzip this bundle alongside your existing DME repository.
2. Copy or move the `dme-platform/` directory into your main Git repo.
3. Move all legacy zip snapshots into `dme-platform/archive/` and mark them
   non-deployable.
4. Wire GitHub Actions to use `.github/workflows/*.yml` from this monorepo.
5. Configure environment variables as per `.env.example`.
6. Run `scripts/setup_dev.sh` then `scripts/run_tests.sh` to validate.
7. Increment your own version in `CHANGELOG.md` and tag the commit.
