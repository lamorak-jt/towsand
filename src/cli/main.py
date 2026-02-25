"""Towsand CLI — root command group and core commands."""

import logging

import click

from src.db.init_schema import init_db
from src.db.seed import seed_cash_balances, seed_institutions_and_accounts, seed_parameters


@click.group()
@click.version_option(version="0.1.0", prog_name="towsand")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
def cli(verbose):
    """Towsand — portfolio management for the Townsend family."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(name)s %(levelname)s: %(message)s")


@cli.command()
def init():
    """Initialise the database: create schema, seed institutions, set parameters."""
    click.echo("Initialising database...")
    init_db()
    click.echo("  Schema created.")

    seed_institutions_and_accounts()
    click.echo("  Institutions and accounts seeded.")

    seed_cash_balances()
    click.echo("  Cash balances seeded.")

    seed_parameters()
    click.echo("  Default parameters set.")

    click.echo("Done. Database ready at data/towsand.db")


# ---------------------------------------------------------------------------
# Prices command group
# ---------------------------------------------------------------------------

@cli.group("prices")
def prices_group():
    """Fetch and manage instrument prices."""


@prices_group.command("update")
def prices_update():
    """Fetch latest prices for all held instruments from yfinance."""
    from src.market_data.price_fetcher import fetch_prices

    click.echo("Fetching latest prices...")
    results = fetch_prices()
    click.echo(f"  Updated: {results['updated']}")
    if results["failed"]:
        click.echo(f"  Failed:  {', '.join(results['failed'])}")


@prices_group.command("history")
@click.argument("ticker")
@click.option("--days", default=1825, help="Number of calendar days to backfill (default 1825 = 5 years).")
def prices_history(ticker, days):
    """Backfill historical daily prices for a single instrument."""
    from src.market_data.price_fetcher import fetch_price_history

    click.echo(f"Backfilling {ticker} ({days} days)...")
    results = fetch_price_history(ticker, days)
    click.echo(f"  Stored {results['rows']} price rows for {results['ticker']}")


@prices_group.command("history-all")
@click.option("--days", default=1825, help="Number of calendar days to backfill (default 1825 = 5 years).")
def prices_history_all(days):
    """Backfill historical prices for ALL held instruments."""
    from src.db.connection import get_connection
    from src.market_data.price_fetcher import fetch_price_history

    with get_connection() as conn:
        tickers = [r["ticker"] for r in conn.execute("""
            SELECT DISTINCT i.ticker
            FROM instruments i JOIN holdings h ON h.instrument_id = i.id
            ORDER BY i.ticker
        """)]

    click.echo(f"Backfilling {len(tickers)} instruments ({days} days each)...")
    total = 0
    for ticker in tickers:
        try:
            results = fetch_price_history(ticker, days)
            click.echo(f"  {ticker:<14s}  {results['rows']:>6,d} rows")
            total += results["rows"]
        except Exception as exc:
            click.echo(f"  {ticker:<14s}  FAILED: {exc}")
    click.echo(f"Total: {total:,d} price rows stored")


@prices_group.command("list")
def prices_list():
    """Show the latest price for each held instrument."""
    from src.db.connection import get_connection

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT i.ticker, p.close_price, p.currency, p.date, p.source,
                   h.quantity,
                   (h.quantity * p.close_price) AS local_value
            FROM instruments i
            JOIN holdings h ON h.instrument_id = i.id
            JOIN prices p ON p.instrument_id = i.id
            WHERE p.date = (
                SELECT MAX(p2.date) FROM prices p2 WHERE p2.instrument_id = i.id
            )
            ORDER BY i.ticker
        """).fetchall()

    if not rows:
        click.echo("No prices stored for held instruments.")
        return

    click.echo(f"{'Ticker':<14s}  {'Price':>10s}  {'Ccy':<4s}  {'Qty':>10s}  "
               f"{'Value':>14s}  {'Date':>12s}  {'Source':<10s}")
    click.echo("-" * 82)
    for r in rows:
        click.echo(f"{r['ticker']:<14s}  {r['close_price']:>10.4f}  {r['currency']:<4s}  "
                   f"{r['quantity']:>10.2f}  {r['local_value']:>14,.2f}  "
                   f"{r['date']:>12s}  {r['source']:<10s}")


# ---------------------------------------------------------------------------
# FX command group
# ---------------------------------------------------------------------------

@cli.group("fx")
def fx_group():
    """Fetch and manage FX rates."""


@fx_group.command("update")
def fx_update():
    """Fetch latest FX rates for all portfolio currencies from yfinance."""
    from src.market_data.price_fetcher import fetch_fx_rates

    click.echo("Fetching latest FX rates...")
    results = fetch_fx_rates()
    click.echo(f"  Updated: {results['updated']}")
    if results["failed"]:
        click.echo(f"  Failed:  {', '.join(results['failed'])}")


@fx_group.command("history")
@click.argument("from_currency")
@click.option("--to", "to_currency", default="AUD", help="Target currency (default AUD).")
@click.option("--days", default=1825, help="Number of calendar days (default 1825 = 5 years).")
def fx_history(from_currency, to_currency, days):
    """Backfill historical FX rates for a currency pair."""
    from src.market_data.price_fetcher import fetch_fx_history

    click.echo(f"Backfilling {from_currency}/{to_currency} ({days} days)...")
    results = fetch_fx_history(from_currency, to_currency, days)
    click.echo(f"  Stored {results['rows']} rate rows for {results['pair']}")


@fx_group.command("history-all")
@click.option("--days", default=1825, help="Number of calendar days (default 1825 = 5 years).")
def fx_history_all(days):
    """Backfill historical FX rates for ALL portfolio currencies."""
    from src.db.connection import get_connection
    from src.market_data.price_fetcher import fetch_fx_history

    with get_connection() as conn:
        base_row = conn.execute(
            "SELECT value FROM parameters WHERE key = 'base_currency'"
        ).fetchone()
        base = base_row["value"] if base_row else "AUD"

        currencies = set()
        for r in conn.execute("SELECT DISTINCT currency FROM instruments"):
            currencies.add(r["currency"])
        for r in conn.execute("SELECT DISTINCT currency FROM cash_balances"):
            currencies.add(r["currency"])
        currencies.discard(base)

    click.echo(f"Backfilling {len(currencies)} FX pairs ({days} days each)...")
    total = 0
    for ccy in sorted(currencies):
        try:
            results = fetch_fx_history(ccy, base, days)
            click.echo(f"  {ccy}/{base:<8s}  {results['rows']:>6,d} rows")
            total += results["rows"]
        except Exception as exc:
            click.echo(f"  {ccy}/{base:<8s}  FAILED: {exc}")
    click.echo(f"Total: {total:,d} FX rate rows stored")


@fx_group.command("list")
def fx_list():
    """Show the latest FX rates in the database."""
    from src.db.connection import get_connection

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT from_currency, to_currency, rate, date, source
            FROM fx_rates
            WHERE (from_currency, date) IN (
                SELECT from_currency, MAX(date)
                FROM fx_rates WHERE to_currency = 'AUD'
                GROUP BY from_currency
            ) AND to_currency = 'AUD'
            ORDER BY from_currency
        """).fetchall()

    if not rows:
        click.echo("No FX rates stored.")
        return

    click.echo(f"{'Pair':<10s}  {'Rate':>10s}  {'Date':>12s}  {'Source':<12s}")
    click.echo("-" * 50)
    for r in rows:
        click.echo(f"{r['from_currency']}/{r['to_currency']:<6s}  {r['rate']:>10.6f}  "
                   f"{r['date']:>12s}  {r['source']:<12s}")


# ---------------------------------------------------------------------------
# Portfolio command group
# ---------------------------------------------------------------------------

@cli.group("portfolio")
def portfolio_group():
    """Portfolio valuation, summary, and classification."""


@portfolio_group.command("value")
@click.option("--by", "group_by", type=click.Choice(["ticker", "account", "institution", "type", "currency", "country"]),
              default="ticker", help="Group holdings by field.")
def portfolio_value(group_by):
    """Show full portfolio valuation with AUD conversion."""
    from src.portfolio.valuation import compute_valuation

    pv = compute_valuation()

    # Holdings table
    click.echo("\n--- Holdings ---")
    click.echo(f"{'Ticker':<14s}  {'Type':<12s}  {'Ccy':<4s}  {'Qty':>10s}  "
               f"{'Price':>10s}  {'Lcl Value':>14s}  {'FX':>8s}  {'AUD Value':>14s}  {'Date':>12s}")
    click.echo("-" * 112)

    for h in pv.holdings:
        click.echo(
            f"{h.ticker:<14s}  {h.instrument_type:<12s}  {h.currency:<4s}  {h.quantity:>10,.2f}  "
            f"{h.price:>10.4f}  {h.local_value:>14,.2f}  {h.fx_rate:>8.4f}  "
            f"{h.value_aud:>14,.2f}  {h.price_date:>12s}"
        )

    click.echo(f"\n{'Holdings total':>78s}  {pv.total_holdings_aud:>14,.2f}")

    # Cash table
    click.echo("\n--- Cash ---")
    click.echo(f"{'Account':<24s}  {'Ccy':<4s}  {'Balance':>14s}  "
               f"{'FX':>8s}  {'AUD Value':>14s}  {'As Of':>12s}")
    click.echo("-" * 84)

    for c in pv.cash:
        excl_mark = "  *" if not c.is_investable else ""
        click.echo(
            f"{c.account_name:<24s}  {c.currency:<4s}  {c.balance:>14,.2f}  "
            f"{c.fx_rate:>8.4f}  {c.value_aud:>14,.2f}  {c.as_of_date:>12s}{excl_mark}"
        )

    click.echo(f"\n{'Investable cash':>56s}  {pv.investable_cash_aud:>14,.2f}")
    if pv.non_investable_cash_aud:
        click.echo(f"{'Non-investable (*)':>56s}  {pv.non_investable_cash_aud:>14,.2f}")
    click.echo(f"{'INVESTABLE TOTAL':>56s}  {pv.total_aud:>14,.2f}")


@portfolio_group.command("summary")
def portfolio_summary():
    """Show portfolio allocation by role, type, currency, country."""
    from src.portfolio.valuation import compute_valuation

    pv = compute_valuation()
    total = pv.total_aud

    def _print_breakdown(title: str, data: dict[str, float]) -> None:
        click.echo(f"\n--- {title} ---")
        sorted_items = sorted(data.items(), key=lambda x: -x[1])
        for label, value in sorted_items:
            pct = (value / total * 100) if total > 0 else 0
            click.echo(f"  {label:<24s}  {value:>14,.2f}  {pct:>6.1f}%")

    click.echo(f"\nInvestable assets: AUD {total:,.2f}")
    click.echo(f"  Holdings:         AUD {pv.total_holdings_aud:,.2f}")
    click.echo(f"  Investable cash:  AUD {pv.investable_cash_aud:,.2f}  (allocated to stabiliser)")
    if pv.non_investable_cash_aud:
        click.echo(f"  Non-investable:   AUD {pv.non_investable_cash_aud:,.2f}  (excluded from compliance)")

    _print_breakdown("By Capital Role (cash → stabiliser)", pv.by_capital_role())
    _print_breakdown("By Instrument Type", pv.by_instrument_type())
    _print_breakdown("By Currency", pv.by_currency())
    _print_breakdown("By Country", pv.by_country())
    _print_breakdown("By Institution", pv.by_institution())


# ---------------------------------------------------------------------------
# Classify command group (instrument classification)
# ---------------------------------------------------------------------------

@cli.group("classify")
def classify_group():
    """Manage instrument classifications (capital role, macro drivers, etc.)."""


@classify_group.command("role")
@click.argument("ticker")
@click.argument("role", type=click.Choice(["stabiliser", "compounder", "optionality"]))
def classify_role(ticker, role):
    """Assign a capital role to an instrument."""
    from src.db.connection import get_connection

    with get_connection() as conn:
        inst = conn.execute("SELECT id FROM instruments WHERE ticker = ?", (ticker,)).fetchone()
        if not inst:
            click.echo(f"Instrument not found: {ticker}")
            return

        existing = conn.execute(
            "SELECT id FROM instrument_classifications WHERE instrument_id = ?",
            (inst["id"],),
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE instrument_classifications SET capital_role = ?, updated_at = datetime('now') "
                "WHERE instrument_id = ?",
                (role, inst["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO instrument_classifications (instrument_id, capital_role) VALUES (?, ?)",
                (inst["id"], role),
            )

    click.echo(f"{ticker} → {role}")


@classify_group.command("tag")
@click.argument("ticker")
@click.option("--macro", "macro_drivers", help="Comma-separated macro drivers (e.g. 'au_housing,bulk_commodities').")
@click.option("--group", "corporate_group", help="Corporate group name.")
@click.option("--corr-group", "corr_group", help="Stress correlation group.")
@click.option("--duration", type=float, help="Duration in years.")
@click.option("--liquidity", type=int, help="Liquidity in days to exit.")
@click.option("--inflation-linked/--no-inflation-linked", default=None, help="Is inflation-linked?")
@click.option("--hedged/--unhedged", default=None, help="Is FX-hedged?")
def classify_tag(ticker, macro_drivers, corporate_group, corr_group, duration,
                 liquidity, inflation_linked, hedged):
    """Tag an instrument with macro drivers, corporate group, and other metadata."""
    import json
    from src.db.connection import get_connection

    with get_connection() as conn:
        inst = conn.execute("SELECT id FROM instruments WHERE ticker = ?", (ticker,)).fetchone()
        if not inst:
            click.echo(f"Instrument not found: {ticker}")
            return

        existing = conn.execute(
            "SELECT id FROM instrument_classifications WHERE instrument_id = ?",
            (inst["id"],),
        ).fetchone()

        if not existing:
            conn.execute(
                "INSERT INTO instrument_classifications (instrument_id) VALUES (?)",
                (inst["id"],),
            )

        updates = []
        params = []
        if macro_drivers is not None:
            drivers_list = [d.strip() for d in macro_drivers.split(",") if d.strip()]
            updates.append("macro_drivers = ?")
            params.append(json.dumps(drivers_list))
        if corporate_group is not None:
            updates.append("corporate_group = ?")
            params.append(corporate_group)
        if corr_group is not None:
            updates.append("stress_correlation_group = ?")
            params.append(corr_group)
        if duration is not None:
            updates.append("duration_years = ?")
            params.append(duration)
        if liquidity is not None:
            updates.append("liquidity_days = ?")
            params.append(liquidity)
        if inflation_linked is not None:
            updates.append("is_inflation_linked = ?")
            params.append(1 if inflation_linked else 0)
        if hedged is not None:
            updates.append("hedged = ?")
            params.append(1 if hedged else 0)

        if updates:
            updates.append("updated_at = datetime('now')")
            params.append(inst["id"])
            conn.execute(
                f"UPDATE instrument_classifications SET {', '.join(updates)} "
                "WHERE instrument_id = ?",
                params,
            )

    applied = [s.split(" = ")[0] for s in updates if "updated_at" not in s]
    click.echo(f"{ticker}: updated {', '.join(applied)}")


@classify_group.command("list")
def classify_list():
    """Show all instruments with their current classification."""
    from src.db.connection import get_connection

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT i.ticker, i.instrument_type, i.currency,
                   ic.capital_role, ic.macro_drivers, ic.corporate_group,
                   ic.stress_correlation_group, ic.duration_years, ic.liquidity_days,
                   ic.is_inflation_linked, ic.hedged
            FROM instruments i
            LEFT JOIN instrument_classifications ic ON ic.instrument_id = i.id
            JOIN holdings h ON h.instrument_id = i.id
            ORDER BY ic.capital_role NULLS LAST, i.ticker
        """).fetchall()

    click.echo(f"{'Ticker':<14s}  {'Type':<12s}  {'Role':<14s}  {'Macro Drivers':<30s}  "
               f"{'Group':<12s}  {'Hedged':<7s}")
    click.echo("-" * 97)
    for r in rows:
        role = r["capital_role"] or "---"
        drivers = r["macro_drivers"] or "---"
        group = r["corporate_group"] or "---"
        hedged_str = "yes" if r["hedged"] == 1 else ("no" if r["hedged"] == 0 else "---")
        click.echo(f"{r['ticker']:<14s}  {r['instrument_type']:<12s}  {role:<14s}  "
                   f"{drivers:<30s}  {group:<12s}  {hedged_str:<7s}")


@portfolio_group.command("exposures")
def portfolio_exposures():
    """Show portfolio exposure to macro drivers and corporate groups."""
    from src.portfolio.valuation import compute_valuation

    pv = compute_valuation()
    total = pv.total_aud

    click.echo(f"\nTotal portfolio: AUD {total:,.2f}")

    macro = pv.by_macro_driver()
    click.echo("\n--- Macro Driver Exposure ---")
    for driver, value in sorted(macro.items(), key=lambda x: -x[1]):
        pct = (value / total * 100) if total > 0 else 0
        click.echo(f"  {driver:<24s}  AUD {value:>14,.2f}  {pct:>6.1f}%")

    # Corporate group from classifications
    groups: dict[str, float] = {}
    for h in pv.holdings:
        grp = h.corporate_group or "ungrouped"
        groups[grp] = groups.get(grp, 0) + h.value_aud

    click.echo("\n--- Corporate Group Concentration ---")
    for grp, value in sorted(groups.items(), key=lambda x: -x[1]):
        pct = (value / total * 100) if total > 0 else 0
        click.echo(f"  {grp:<24s}  AUD {value:>14,.2f}  {pct:>6.1f}%")


# ---------------------------------------------------------------------------
# Config command group
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Compliance command
# ---------------------------------------------------------------------------

@cli.command("compliance")
@click.option("--detail", is_flag=True, help="Show full detail per rule.")
@click.option("--save/--no-save", default=True, help="Store result as a compliance snapshot.")
def compliance_cmd(detail, save):
    """Run all compliance checks against portfolio management rules."""
    from src.portfolio.valuation import compute_valuation
    from src.compliance.checks import run_all_checks, store_compliance_snapshot

    pv = compute_valuation()
    results = run_all_checks(pv)

    # Summary counts
    passes = sum(1 for r in results if r.status == "pass")
    warnings = sum(1 for r in results if r.status == "warning")
    breaches = sum(1 for r in results if r.status == "breach")

    click.echo(f"\nPortfolio: AUD {pv.total_aud:,.2f}")
    click.echo(f"Compliance: {passes} pass, {warnings} warning, {breaches} breach\n")

    status_icon = {"pass": "✓", "warning": "⚠", "breach": "✗"}
    status_color = {"pass": "green", "warning": "yellow", "breach": "red"}

    if detail:
        for r in results:
            icon = status_icon[r.status]
            click.echo(click.style(
                f"  {icon} [{r.rule_id}] {r.rule_name}: {r.detail}",
                fg=status_color[r.status],
            ))
    else:
        # Show warnings and breaches only
        for r in results:
            if r.status != "pass":
                icon = status_icon[r.status]
                click.echo(click.style(
                    f"  {icon} [{r.rule_id}] {r.rule_name}: {r.detail}",
                    fg=status_color[r.status],
                ))
        if warnings == 0 and breaches == 0:
            click.echo(click.style("  All checks passed.", fg="green"))

    if save:
        snap_id = store_compliance_snapshot(results, pv.total_aud)
        click.echo(f"\nSnapshot #{snap_id} saved.")


# ---------------------------------------------------------------------------
# Analytics commands (sensitivity, stress, correlations)
# ---------------------------------------------------------------------------

@cli.command("sensitivity")
@click.option("--trades", "trades_file", type=click.Path(exists=True),
              help="JSON file of hypothetical trades. Shows pre-trade AND post-trade sensitivity.")
def sensitivity_cmd(trades_file):
    """How fragile is the portfolio against its strategic objectives?

    Tests: income bridge failure, forced liquidation distance, compounding
    capital at risk, AUD liability matching, optionality sizing.

    With --trades <file.json>, shows both pre-trade and post-trade sensitivity.
    JSON format: [{"ticker": "FLBL", "delta_aud": -120000}, ...]
    """
    import json as json_mod
    from src.portfolio.valuation import compute_valuation, project_valuation
    from src.analytics.sensitivity import analyse_sensitivity

    pv = compute_valuation()

    projected_pv = None
    if trades_file:
        with open(trades_file) as f:
            trades = json_mod.load(f)
        projected_pv = project_valuation(pv, trades)

    portfolios = [("PRE-TRADE", pv)]
    if projected_pv:
        portfolios.append(("POST-TRADE", projected_pv))

    severity_color = {"safe": "green", "watch": "cyan", "fragile": "yellow", "critical": "red"}
    severity_icon = {"safe": "✓", "watch": "◉", "fragile": "⚠", "critical": "✗"}

    for label, port in portfolios:
        report = analyse_sensitivity(port)
        label_str = f" ({label})" if projected_pv else ""

        click.echo(f"\nPortfolio{label_str}: AUD {port.total_aud:,.2f}")
        click.echo(click.style(f"\n=== OBJECTIVE-LEVEL SENSITIVITY{label_str} ===\n", bold=True))

        for obj in report.objectives:
            color = severity_color.get(obj.severity, "white")
            icon = severity_icon.get(obj.severity, "?")
            click.echo(click.style(
                f"  {icon} {obj.objective} [{obj.severity.upper()}]",
                fg=color, bold=obj.severity in ("critical", "fragile"),
            ))
            click.echo(f"    {obj.headline}")
            click.echo(click.style(f"    State: {obj.current_state}", dim=True))
            click.echo(f"    Trigger: {obj.trigger_move}")
            click.echo(f"    Consequence: {obj.consequence}")
            click.echo()

        if report.rule_buffers:
            click.echo(click.style(f"--- Supporting: Rule-Level Buffers{label_str} ---\n", bold=True))
            click.echo(f"  {'Rule':<10s}  {'Description':<26s}  {'Current':>8s}  {'Limit':>6s}  {'Buffer':>7s}  {'Move'}")
            click.echo(f"  {'-'*90}")
            for rb in report.rule_buffers:
                click.echo(
                    f"  {rb.rule_id:<10s}  {rb.description:<26s}  {rb.current_value:>7.1f}%  "
                    f"{rb.limit:>5.0f}%  {rb.buffer_pct:>+6.1f}pp  {rb.breach_move}"
                )


@cli.command("stress")
@click.option("--scenario", type=click.Choice(["flat35", "covid2020", "gfc2008", "rates2022", "all"]),
              default="all", help="Scenario to run (default: all).")
@click.option("--detail", is_flag=True, help="Show per-holding drawdowns.")
@click.option("--trades", "trades_file", type=click.Path(exists=True),
              help="JSON file of hypothetical trades to project. Runs pre-trade AND post-trade comparison.")
def stress_cmd(scenario, detail, trades_file):
    """What happens to your strategic objectives under stress?

    For each scenario: can you still feed your family? How much compounding
    was destroyed? Did optionality pay off? Are you forced to sell?

    With --trades <file.json>, runs both pre-trade and post-trade portfolios
    and shows how the trades change resilience. JSON format:
    [{"ticker": "FLBL", "delta_aud": -120000}, {"ticker": "VAS.AX", "delta_aud": 80000}]
    """
    import json as json_mod
    from src.portfolio.valuation import compute_valuation, project_valuation
    from src.analytics.stress import run_scenario, run_all_scenarios

    pv = compute_valuation()

    projected_pv = None
    if trades_file:
        with open(trades_file) as f:
            trades = json_mod.load(f)
        projected_pv = project_valuation(pv, trades)

    portfolios = [("PRE-TRADE", pv)]
    if projected_pv:
        portfolios.append(("POST-TRADE", projected_pv))

    all_run_results: list[tuple[str, list]] = []

    for label, port in portfolios:
        if scenario == "all":
            results = run_all_scenarios(port)
        else:
            results = [run_scenario(port, scenario)]
        all_run_results.append((label, results))

    # If comparing, show side-by-side summary
    if projected_pv:
        click.echo(f"\nPre-trade portfolio:  AUD {pv.total_aud:,.2f}")
        click.echo(f"Post-trade portfolio: AUD {projected_pv.total_aud:,.2f}")
        click.echo(click.style("\n=== PRE-TRADE vs POST-TRADE STRESS COMPARISON ===\n", bold=True))

        pre_results = {r.scenario_id: r for _, r_list in all_run_results[:1] for r in r_list}
        post_results = {r.scenario_id: r for _, r_list in all_run_results[1:] for r in r_list}

        click.echo(f"  {'Scenario':<30s}  {'| Pre-Trade':>44s}  {'| Post-Trade':>44s}  {'| Delta':>20s}")
        click.echo(f"  {'':<30s}  {'Wealth Loss':>12s} {'Comp.Dam':>10s} {'Recov':>8s} {'Forced':>8s}"
                   f"  {'Wealth Loss':>12s} {'Comp.Dam':>10s} {'Recov':>8s} {'Forced':>8s}"
                   f"  {'Comp.':>10s} {'Recov':>8s}")
        click.echo(f"  {'-'*170}")

        for sid in (pre_results.keys() | post_results.keys()):
            pre = pre_results.get(sid)
            post = post_results.get(sid)
            if not pre or not post:
                continue
            po, qo = pre.objectives, post.objectives

            pre_forced = "YES" if po.forced_liquidation else "No"
            post_forced = "YES" if qo.forced_liquidation else "No"
            comp_delta = qo.compounder_loss_aud - po.compounder_loss_aud
            recov_delta = qo.recovery_years - po.recovery_years
            d_sign = "+" if comp_delta > 0 else ""
            r_sign = "+" if recov_delta > 0 else ""

            click.echo(
                f"  {pre.scenario_name:<30s}  "
                f"{po.wealth_loss_aud:>12,.0f} {po.compounder_loss_aud:>10,.0f} {po.recovery_years:>7.1f}y {pre_forced:>8s}"
                f"  {qo.wealth_loss_aud:>12,.0f} {qo.compounder_loss_aud:>10,.0f} {qo.recovery_years:>7.1f}y {post_forced:>8s}"
                f"  {d_sign}{comp_delta:>9,.0f} {r_sign}{recov_delta:>7.1f}y"
            )
        click.echo()

    # Per-portfolio detail
    for label, results in all_run_results:
        port = pv if label == "PRE-TRADE" else projected_pv
        label_str = f" ({label})" if projected_pv else ""

        click.echo(click.style(f"\n=== STRESS SCENARIOS{label_str}: AUD {port.total_aud:,.2f} ===\n", bold=True))

        # Summary table
        click.echo(f"  {'Scenario':<38s}  {'Wealth Loss':>12s}  {'Comp. Damage':>14s}  {'Recovery':>10s}  {'Forced Sell?'}")
        click.echo(f"  {'-'*100}")
        for r in results:
            o = r.objectives
            forced = click.style("YES", fg="red", bold=True) if o.forced_liquidation else click.style("No", fg="green")
            click.echo(
                f"  {r.scenario_name:<38s}  "
                f"AUD {o.wealth_loss_aud:>10,.0f}  "
                f"AUD {o.compounder_loss_aud:>12,.0f}  "
                f"{o.recovery_years:>8.1f} yrs  "
                f"{forced}"
            )

        # Detail per scenario
        for r in results:
            o = r.objectives
            click.echo(f"\n{'='*70}")
            click.echo(click.style(f"  {r.scenario_name}{label_str}", bold=True))
            click.echo(f"  {r.description}")
            if r.data_source_note:
                click.echo(click.style(f"  [{r.data_source_note}]", dim=True))
            click.echo()

            color = "red" if o.forced_liquidation else "green"
            icon = "✗" if o.forced_liquidation else "✓"
            click.echo(click.style(f"  {icon} SURVIVABILITY: {o.forced_liquidation_detail}", fg=color))

            color = "red" if not o.income_bridge_intact else "green"
            click.echo(click.style(
                f"  {'✗' if not o.income_bridge_intact else '✓'} INCOME BRIDGE: "
                f"{o.income_bridge_months_post:.0f} months covered "
                f"(was {o.income_bridge_months_pre:.0f}, lost {o.income_bridge_months_lost:.0f})",
                fg=color,
            ))

            if o.compounder_loss_aud > 0:
                click.echo(click.style(
                    f"  ⚠ COMPOUNDING: Lost AUD {o.compounder_loss_aud:,.0f} "
                    f"({o.compounder_loss_pct:.0f}% of compounders). "
                    f"Recovery: {o.recovery_years:.1f} years at 6.5% real.",
                    fg="yellow",
                ))
            else:
                click.echo(click.style("  ✓ COMPOUNDING: No compounder loss.", fg="green"))

            if o.optionality_pre_aud > 0:
                opt_word = "gained" if o.optionality_change_pct > 0 else "lost"
                color = "green" if o.optionality_performed else "yellow"
                performed = "performed" if o.optionality_performed else "did NOT offset"
                click.echo(click.style(
                    f"  {'✓' if o.optionality_performed else '⚠'} OPTIONALITY: "
                    f"{opt_word} {abs(o.optionality_change_pct):.0f}% "
                    f"(AUD {o.optionality_pre_aud:,.0f} → {o.optionality_post_aud:,.0f}). "
                    f"Crisis insurance {performed}.",
                    fg=color,
                ))

            click.echo(
                f"  ◉ REAL WEALTH: AUD {o.total_pre_aud:,.0f} → {o.total_post_aud:,.0f} "
                f"({o.wealth_loss_pct:+.1f}%, AUD {o.wealth_loss_aud:,.0f} lost)"
            )

            if detail:
                click.echo("\n  Per-holding drawdowns:")
                click.echo(f"  {'Ticker':<14s}  {'Role':<12s}  {'Pre':>12s}  {'DD':>8s}  {'Post':>12s}  {'Source':<10s}")
                click.echo(f"  {'-'*74}")
                for hs in sorted(r.holding_stresses, key=lambda x: x.drawdown_pct):
                    role = hs.capital_role or "—"
                    click.echo(
                        f"  {hs.ticker:<14s}  {role:<12s}  {hs.pre_stress_aud:>12,.0f}  "
                        f"{hs.drawdown_pct:>+7.1f}%  {hs.post_stress_aud:>12,.0f}  {hs.source:<10s}"
                    )

            if r.breaches:
                click.echo(click.style(f"\n  Rule breaches under stress ({len(r.breaches)}):", dim=True))
                for b in r.breaches:
                    click.echo(click.style(f"    [{b.rule_id}] {b.detail}", dim=True))


@cli.command("correlations")
@click.option("--window", type=click.Choice(["60", "252"]), default="252",
              help="Rolling window in trading days (default: 252).")
@click.option("--stress-only", is_flag=True, help="Only show stress-period correlations.")
@click.option("--detail", is_flag=True, help="Show full pairwise table and group validation.")
def correlations_cmd(window, stress_only, detail):
    """Does your diversification actually work when it matters?

    Tests: does the stabiliser stabilise in a crisis? Does optionality
    provide crisis alpha? Are compounders truly diversified or secretly
    the same bet?
    """
    from src.portfolio.valuation import compute_valuation
    from src.analytics.correlation import compute_correlations

    pv = compute_valuation()
    win = int(window)

    click.echo(f"\nComputing {win}-day rolling correlations...")
    report = compute_correlations(pv, window=win, stress_only=stress_only)
    click.echo(f"Stress periods identified: {report.stress_periods_used} trading days\n")

    # === OBJECTIVE-LEVEL ASSESSMENTS ===
    click.echo(click.style("=== DOES YOUR DIVERSIFICATION WORK? ===\n", bold=True))

    assess_color = {"protective": "green", "neutral": "cyan", "co-moving": "red", "unknown": "white"}
    assess_icon = {"protective": "✓", "neutral": "◉", "co-moving": "✗", "unknown": "?"}
    div_color = {"well-diversified": "green", "moderate": "cyan", "concentrated": "yellow",
                 "false diversification": "red", "N/A": "white", "unknown": "white"}

    # 1. Does stabiliser protect?
    if report.stabiliser_protects:
        a = report.stabiliser_protects
        color = assess_color.get(a.assessment, "white")
        icon = assess_icon.get(a.assessment, "?")
        click.echo(click.style(f"  {icon} STABILISER PROTECTION [{a.assessment.upper()}]", fg=color, bold=True))
        click.echo(f"    {a.detail}")
        click.echo()

    # 2. Does optionality perform?
    if report.optionality_performs:
        a = report.optionality_performs
        color = assess_color.get(a.assessment, "white")
        icon = assess_icon.get(a.assessment, "?")
        click.echo(click.style(f"  {icon} OPTIONALITY AS CRISIS INSURANCE [{a.assessment.upper()}]", fg=color, bold=True))
        click.echo(f"    {a.detail}")
        click.echo()

    # 3. Compounder diversification
    if report.compounder_diversity:
        d = report.compounder_diversity
        color = div_color.get(d.assessment, "white")
        click.echo(click.style(f"  ◉ COMPOUNDER DIVERSIFICATION [{d.assessment.upper()}]", fg=color, bold=True))
        click.echo(f"    {d.detail}")
        if d.highest_pair != "N/A":
            click.echo(f"    Most correlated pair: {d.highest_pair}")
        click.echo()

    # All role diversifications
    for rd in report.role_diversifications:
        if rd.role == "compounder":
            continue  # already shown
        color = div_color.get(rd.assessment, "white")
        click.echo(click.style(f"  ◉ {rd.role.upper()} DIVERSIFICATION [{rd.assessment.upper()}]", fg=color))
        click.echo(f"    {rd.detail}")
        click.echo()

    # Flagged pairs that matter
    flagged = [p for p in report.pair_results if p.flag is not None]
    if flagged:
        click.echo(click.style(f"--- Actionable Findings ({len(flagged)} pairs) ---\n", bold=True))
        for p in flagged:
            icon = "⚠" if p.flag == "over-grouped" else "🔍"
            color = "yellow" if p.flag == "over-grouped" else "cyan"
            click.echo(click.style(f"  {icon} {p.detail}", fg=color))
        click.echo()

    if not detail:
        return

    # Supporting: group validation
    click.echo(click.style("--- Supporting: Stress Group Tag Validation ---\n", bold=True))
    for gv in report.group_validations:
        icon = "✓" if gv.valid else "✗"
        color = "green" if gv.valid else "red"
        click.echo(click.style(f"  {icon} {gv.group_name}: {', '.join(gv.tickers)}", fg=color))
        click.echo(f"    {gv.detail}  Weakest: {gv.weakest_pair}")

    # Supporting: full pairwise table
    click.echo(click.style("\n--- Supporting: Top Pairwise Correlations ---\n", bold=True))
    click.echo(f"  {'Pair':<28s}  {'Role A':<12s}  {'Role B':<12s}  {'60d':>6s}  {'Stress':>7s}  {'Flag'}")
    click.echo(f"  {'-'*85}")
    sorted_pairs = sorted(
        report.pair_results,
        key=lambda p: -(abs(p.corr_stress) if p.corr_stress is not None
                        else abs(p.corr_60d) if p.corr_60d is not None else 0),
    )
    for p in sorted_pairs[:25]:
        ra = p.role_a or "—"
        rb = p.role_b or "—"
        c60 = f"{p.corr_60d:.2f}" if p.corr_60d is not None else "—"
        cstr = f"{p.corr_stress:.2f}" if p.corr_stress is not None else "—"
        flag = p.flag or ""
        click.echo(f"  {p.ticker_a}–{p.ticker_b:<25s}  {ra:<12s}  {rb:<12s}  {c60:>6s}  {cstr:>7s}  {flag}")


@cli.group("config")
def config_group():
    """Manage stored credentials and settings (~/.config/towsand/credentials)."""


@config_group.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Store a credential value (e.g. ib_token, ib_query_id)."""
    from src import config

    config.set_value(key, value)
    desc = config.KNOWN_KEYS.get(key, "")
    label = f" ({desc})" if desc else ""
    click.echo(f"Stored '{key}'{label} in {config.CREDENTIALS_FILE}")


@config_group.command("get")
@click.argument("key")
def config_get(key):
    """Retrieve a credential value (checks env var, then credentials file)."""
    from src import config

    val = config.get(key)
    if val is None:
        click.echo(f"'{key}' is not set.")
        raise SystemExit(1)
    masked = val[:4] + "..." + val[-4:] if len(val) > 12 else "****"
    click.echo(f"{key} = {masked}")


@config_group.command("delete")
@click.argument("key")
def config_delete(key):
    """Remove a stored credential."""
    from src import config

    if config.delete(key):
        click.echo(f"Deleted '{key}'.")
    else:
        click.echo(f"'{key}' was not set.")


@config_group.command("list")
def config_list():
    """List all stored credentials (values are masked)."""
    from src import config

    stored = config.list_all()
    if not stored:
        click.echo("No credentials stored.")
        click.echo(f"  File: {config.CREDENTIALS_FILE}")
        return
    click.echo(f"Credentials in {config.CREDENTIALS_FILE}:")
    for key, val in stored.items():
        masked = val[:4] + "..." + val[-4:] if len(val) > 12 else "****"
        desc = config.KNOWN_KEYS.get(key, "")
        label = f"  # {desc}" if desc else ""
        click.echo(f"  {key} = {masked}{label}")


@config_group.command("path")
def config_path():
    """Show the credentials file path."""
    from src import config

    click.echo(config.CREDENTIALS_FILE)


# ---------------------------------------------------------------------------
# IB command group
# ---------------------------------------------------------------------------

@cli.group("ib")
def ib_group():
    """Interactive Brokers data import commands."""


@ib_group.command("import-flex")
@click.option("--token", default=None, help="Flex Web Service token (or set via: towsand config set ib_token).")
@click.option("--query-id", default=None, help="Flex Query ID (or set via: towsand config set ib_query_id).")
@click.option("--save-xml", type=click.Path(), default=None,
              help="Save the raw XML report to this path for future use.")
def ib_import_flex(token, query_id, save_xml):
    """Download and import an IB Flex report (positions, cash, FX rates).

    Token and query ID are resolved in order: --flag > env var > stored credential.
    Store them once with: towsand config set ib_token YOUR_TOKEN
    """
    from src import config
    from src.market_data.flex_report import fetch_flex_report
    from src.market_data.ib_importer import import_all

    resolved_token = config.resolve_ib_token(token)
    resolved_qid = config.resolve_ib_query_id(query_id)

    if not resolved_token:
        click.echo("Error: No IB token found. Provide --token or run:")
        click.echo("  towsand config set ib_token YOUR_TOKEN")
        raise SystemExit(1)
    if not resolved_qid:
        click.echo("Error: No IB query ID found. Provide --query-id or run:")
        click.echo("  towsand config set ib_query_id YOUR_QUERY_ID")
        raise SystemExit(1)

    click.echo(f"Downloading Flex report (query {resolved_qid})...")
    report = fetch_flex_report(token=resolved_token, query_id=resolved_qid)
    click.echo(f"  Available topics: {report.available_topics}")

    if save_xml:
        report.save(save_xml)
        click.echo(f"  Raw XML saved to {save_xml}")

    click.echo("Importing into database...")
    results = import_all(report)
    _print_import_results(results)


@ib_group.command("import-file")
@click.argument("xml_path", type=click.Path(exists=True))
def ib_import_file(xml_path):
    """Import positions from a previously saved IB Flex XML file."""
    from src.market_data.flex_report import load_flex_report
    from src.market_data.ib_importer import import_all

    click.echo(f"Loading Flex report from {xml_path}...")
    report = load_flex_report(xml_path)
    click.echo(f"  Available topics: {report.available_topics}")

    click.echo("Importing into database...")
    results = import_all(report)
    _print_import_results(results)


@ib_group.command("topics")
@click.argument("xml_path", type=click.Path(exists=True))
def ib_topics(xml_path):
    """List available topics in a saved Flex XML report (for exploration)."""
    from src.market_data.flex_report import load_flex_report

    report = load_flex_report(xml_path)
    for topic in sorted(report.available_topics):
        click.echo(f"  {topic}")


@ib_group.command("preview")
@click.argument("xml_path", type=click.Path(exists=True))
@click.argument("topic")
@click.option("--rows", default=10, help="Number of rows to display.")
def ib_preview(xml_path, topic, rows):
    """Preview a topic from a saved Flex XML report as a table."""
    from src.market_data.flex_report import load_flex_report

    report = load_flex_report(xml_path)
    df = report.raw_df(topic)
    if df.empty:
        click.echo(f"No data for topic '{topic}'.")
        return
    click.echo(f"Topic '{topic}': {len(df)} rows, {len(df.columns)} columns")
    click.echo(f"Columns: {list(df.columns)}")
    click.echo()
    click.echo(df.head(rows).to_string(index=False))


def _print_import_results(results: dict) -> None:
    """Print a human-readable summary of import results."""
    pos = results.get("positions", {})
    cash = results.get("cash", {})
    fx = results.get("fx", {})

    skipped = pos.get("skipped", 0)
    closed = pos.get("closed", 0)
    skipped_msg = f", {skipped} skipped" if skipped else ""
    closed_msg = f", {closed} closed positions removed" if closed else ""
    click.echo("Import complete:")
    click.echo(f"  Positions: {pos.get('holdings', 0)} holdings, "
               f"{pos.get('instruments', 0)} instruments, "
               f"{pos.get('prices', 0)} prices{skipped_msg}{closed_msg}")
    click.echo(f"  Cash:      {cash.get('balances', 0)} currency balances")
    click.echo(f"  FX rates:  {fx.get('rates', 0)} rates")


# ---------------------------------------------------------------------------
# CommSec command group
# ---------------------------------------------------------------------------

@cli.group("commsec")
def commsec_group():
    """CommSec data import commands."""


@commsec_group.command("import")
@click.argument("csv_path", type=click.Path(exists=True))
def commsec_import(csv_path):
    """Import CommSec holdings from a CSV portfolio export."""
    from src.market_data.commsec_importer import import_commsec_csv

    click.echo(f"Importing CommSec CSV from {csv_path}...")
    results = import_commsec_csv(csv_path)
    skipped = results.get("skipped", 0)
    skipped_msg = f", {skipped} skipped" if skipped else ""
    click.echo(f"Import complete: {results['holdings']} holdings, "
               f"{results['instruments']} instruments, "
               f"{results['prices']} prices{skipped_msg}")


# ---------------------------------------------------------------------------
# Cash command group
# ---------------------------------------------------------------------------

@cli.group("cash")
def cash_group():
    """Manage cash balances across accounts."""


@cash_group.command("update")
@click.argument("account_name")
@click.argument("balance", type=float)
@click.option("--currency", default=None, help="Currency code (default: account's currency).")
def cash_update(account_name, balance, currency):
    """Update a cash balance for an account.

    ACCOUNT_NAME can be a partial match (e.g. 'bonus' matches 'Jacob RACQ Bonus Saver').

    Examples:
        towsand cash update "Jacob RACQ Bonus Saver" 82000
        towsand cash update "bonus saver" 82000
        towsand cash update "wise eur" 5800 --currency EUR
    """
    from datetime import date

    from src.db.connection import get_connection

    with get_connection() as conn:
        search = f"%{account_name}%"
        matches = conn.execute(
            "SELECT id, name, currency FROM accounts WHERE name LIKE ?", (search,)
        ).fetchall()

        if len(matches) == 0:
            click.echo(f"No account found matching '{account_name}'.")
            click.echo("Available accounts:")
            for r in conn.execute("SELECT name FROM accounts ORDER BY name"):
                click.echo(f"  {r['name']}")
            raise SystemExit(1)
        if len(matches) > 1:
            click.echo(f"Multiple accounts match '{account_name}':")
            for r in matches:
                click.echo(f"  {r['name']}")
            click.echo("Please be more specific.")
            raise SystemExit(1)

        acct = matches[0]
        ccy = currency or acct["currency"]
        today = date.today().isoformat()

        old = conn.execute(
            "SELECT balance, as_of_date FROM cash_balances "
            "WHERE account_id = ? AND currency = ? ORDER BY as_of_date DESC LIMIT 1",
            (acct["id"], ccy),
        ).fetchone()

        conn.execute(
            "INSERT OR REPLACE INTO cash_balances (account_id, currency, balance, as_of_date) "
            "VALUES (?, ?, ?, ?)",
            (acct["id"], ccy, balance, today),
        )

        old_str = f"{old['balance']:,.2f} ({old['as_of_date']})" if old else "none"
        click.echo(f"Updated {acct['name']}:")
        click.echo(f"  {ccy} {old_str} → {balance:,.2f} ({today})")


@cash_group.command("list")
def cash_list():
    """Show all cash balances."""
    from src.db.connection import get_connection

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT a.name, cb.currency, cb.balance, cb.as_of_date
            FROM cash_balances cb
            JOIN accounts a ON cb.account_id = a.id
            ORDER BY cb.balance DESC
        """).fetchall()

        if not rows:
            click.echo("No cash balances recorded.")
            return

        click.echo(f"{'Account':<30s}  {'Ccy':>4s}  {'Balance':>14s}  {'As Of':>12s}")
        click.echo("-" * 68)
        for r in rows:
            click.echo(f"{r['name']:<30s}  {r['currency']:>4s}  {r['balance']:>14,.2f}  {r['as_of_date']:>12s}")
