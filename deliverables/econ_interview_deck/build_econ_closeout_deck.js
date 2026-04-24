const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers/layout");

function parseCsv(filePath) {
  const raw = fs.readFileSync(filePath, "utf8").replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
  const lines = raw.split("\n").filter((line) => line.trim().length > 0);
  const header = parseCsvLine(lines[0]);

  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    const row = {};
    for (let i = 0; i < header.length; i += 1) {
      row[header[i]] = (values[i] ?? "").trim();
    }
    return row;
  });
}

function parseCsvLine(line) {
  const values = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }
    if (char === "," && !inQuotes) {
      values.push(current.trim());
      current = "";
      continue;
    }
    current += char;
  }

  if (inQuotes) {
    throw new Error(`Malformed CSV row with unclosed quote: ${line}`);
  }
  values.push(current.trim());
  return values;
}

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : NaN;
}

function pickModel(rows, model, outcome, key) {
  const row = rows.find((item) => item.model === model && item.outcome === outcome);
  if (!row) {
    throw new Error(`Missing model row: model=${model}, outcome=${outcome}`);
  }
  return toNumber(row[key]);
}

function pickCheck(rows, checkName) {
  const row = rows.find((item) => item.check === checkName);
  if (!row) {
    throw new Error(`Missing data audit check: ${checkName}`);
  }
  return toNumber(row.value);
}

function pickMetric(rows, metricName) {
  const row = rows.find((item) => item.metric === metricName);
  if (!row) {
    throw new Error(`Missing metric: ${metricName}`);
  }
  return toNumber(row.value);
}

function loadMetrics() {
  const projectRoot = path.resolve(__dirname, "../..");
  const corePath = path.join(projectRoot, "v2/outputs/phase1_audit_v2/tables/core_model_results_v2.csv");
  const firstStagePath = path.join(projectRoot, "v2/outputs/phase1_audit_v2/tables/first_stage_strength_v2.csv");
  const dataSummaryPath = path.join(projectRoot, "v2/outputs/phase1_audit_v2/tables/data_audit_summary_v2.csv");
  const phase2MetricsPath = path.join(projectRoot, "v2/outputs/phase2_short_run_v2/tables/phase2_interpretation_metrics_v2.csv");

  const coreRows = parseCsv(corePath);
  const firstStageRows = parseCsv(firstStagePath);
  const dataSummaryRows = parseCsv(dataSummaryPath);
  const phase2Rows = parseCsv(phase2MetricsPath);

  const firstStageRow = firstStageRows.find(
    (row) => row.instrument === "instrument_m2_external_level" && row.outcome === "inflation"
  );
  if (!firstStageRow) {
    throw new Error("Missing first-stage row for external IV inflation model");
  }

  return {
    countries: pickCheck(dataSummaryRows, "countries"),
    yearMin: pickCheck(dataSummaryRows, "year_min"),
    yearMax: pickCheck(dataSummaryRows, "year_max"),
    rows: pickCheck(dataSummaryRows, "rows"),
    duplicateRows: pickCheck(dataSummaryRows, "duplicate_country_year_rows"),
    feInflation: pickModel(coreRows, "fe_baseline_twfe", "inflation", "coef_m2_growth"),
    feGdp: pickModel(coreRows, "fe_baseline_twfe", "gdp_growth", "coef_m2_growth"),
    ivInflation: pickModel(coreRows, "iv_twfe_external", "inflation", "coef_m2_growth"),
    ivGdp: pickModel(coreRows, "iv_twfe_external", "gdp_growth", "coef_m2_growth"),
    firstStageStat: toNumber(firstStageRow.first_stage_stat),
    inflationSigHorizons: pickMetric(phase2Rows, "inflation_sig_horizons_primary"),
    gdpSigHorizons: pickMetric(phase2Rows, "gdp_sig_horizons_primary"),
    meanFirstStagePrimary: pickMetric(phase2Rows, "mean_first_stage_stat_primary"),
  };
}

const metrics = loadMetrics();

const now = new Date();
const yyyy = now.getFullYear();
const mm = String(now.getMonth() + 1).padStart(2, "0");
const dd = String(now.getDate()).padStart(2, "0");
const dateLabel = `${yyyy}-${mm}-${dd}`;

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Steven Chung";
pptx.company = "Econometrics Side Project";
pptx.subject = "Money Growth, Inflation, and GDP Growth";
pptx.title = "Cross-Country Money Growth Project - V2 Closeout";
pptx.lang = "en-CA";
pptx.theme = {
  headFontFace: "Aptos Display",
  bodyFontFace: "Aptos",
  lang: "en-CA",
};

function finalizeSlide(slide) {
  warnIfSlideHasOverlaps(slide, pptx);
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

function addHeader(slide, title, subtitle = "") {
  slide.background = { color: "F7F8FA" };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 0.85,
    fill: { color: "1E3A5F" },
    line: { color: "1E3A5F" },
  });
  slide.addText(title, {
    x: 0.55,
    y: 0.18,
    w: 8.2,
    h: 0.38,
    fontFace: "Aptos Display",
    fontSize: 21,
    bold: true,
    color: "FFFFFF",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 9.2,
      y: 0.22,
      w: 3.75,
      h: 0.30,
      align: "right",
      fontFace: "Aptos",
      fontSize: 11,
      color: "D9E2F2",
      italic: true,
    });
  }
}

function addDivider(slide, y = 1.1) {
  slide.addShape(pptx.ShapeType.line, {
    x: 0.55,
    y,
    w: 12.2,
    h: 0,
    line: { color: "D5DCE6", pt: 1.1 },
  });
}

// Slide 1
{
  const slide = pptx.addSlide();
  addHeader(slide, "V2 Closeout: Money Growth, Inflation, and Growth", "Interview Deck | 5 Slides");

  slide.addText("Question", {
    x: 0.7,
    y: 1.25,
    w: 2.2,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText("Across countries, how strongly is money growth linked to inflation and GDP growth?", {
    x: 0.7,
    y: 1.6,
    w: 12.0,
    h: 0.7,
    fontSize: 21,
    bold: true,
    color: "102A43",
    valign: "top",
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.7,
    y: 2.55,
    w: 11.95,
    h: 2.1,
    rectRadius: 0.07,
    fill: { color: "EAF2FB" },
    line: { color: "BBD0EA", pt: 1 },
  });
  slide.addText("One-sentence closeout claim", {
    x: 1.0,
    y: 2.82,
    w: 4.0,
    h: 0.35,
    fontSize: 13,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText(
    "Inflation association is strong and policy-relevant, GDP effects stay weak, and first-stage strength remains modest; this is a disciplined associational portfolio result, not a final causal elasticity.",
    {
      x: 1.0,
      y: 3.28,
      w: 11.2,
      h: 1.25,
      fontSize: 17,
      color: "102A43",
      valign: "top",
      lineSpacingMultiple: 1.12,
    }
  );

  slide.addText("Status: Closed (Phase Complete, Next Phase Optional)", {
    x: 0.8,
    y: 6.78,
    w: 12.0,
    h: 0.3,
    fontSize: 11,
    bold: true,
    color: "334E68",
    align: "right",
  });

  finalizeSlide(slide);
}

// Slide 2
{
  const slide = pptx.addSlide();
  addHeader(slide, "Data and Empirical Design", "V2 frozen evidence");
  addDivider(slide, 1.03);

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.7,
    y: 1.3,
    w: 4.0,
    h: 4.9,
    rectRadius: 0.05,
    fill: { color: "FFFFFF" },
    line: { color: "D5DCE6", pt: 1 },
  });
  slide.addText("Panel Snapshot", {
    x: 1.0,
    y: 1.55,
    w: 2.2,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText(
    [
      { text: `Countries: ${metrics.countries}\n`, options: { breakLine: true } },
      { text: `Years: ${metrics.yearMin}-${metrics.yearMax}\n`, options: { breakLine: true } },
      { text: `Rows: ${metrics.rows.toLocaleString()}\n`, options: { breakLine: true } },
      { text: `Duplicate country-year rows: ${metrics.duplicateRows}`, options: { breakLine: false } },
    ],
    {
      x: 1.0,
      y: 2.05,
      w: 3.45,
      h: 2.1,
      fontSize: 15,
      color: "102A43",
      valign: "top",
      lineSpacingMultiple: 1.15,
    }
  );

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 5.05,
    y: 1.3,
    w: 7.6,
    h: 4.9,
    rectRadius: 0.05,
    fill: { color: "FFFFFF" },
    line: { color: "D5DCE6", pt: 1 },
  });
  slide.addText("Methods Used", {
    x: 5.35,
    y: 1.55,
    w: 2.2,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText(
    "1. TWFE baseline and restricted-controls models\n2. IV-TWFE with lag and external instruments\n3. LP-IV short-run horizons for inflation (h=0..3)\n4. GDP kept static at h=0 by design\n5. Audit-gate logic with explicit weak-IV caveat",
    {
      x: 5.35,
      y: 2.02,
      w: 6.95,
      h: 3.55,
      fontSize: 15,
      color: "102A43",
      valign: "top",
      lineSpacingMultiple: 1.18,
    }
  );

  slide.addText("Objective: evidence quality > result hunting", {
    x: 0.9,
    y: 6.45,
    w: 11.8,
    h: 0.35,
    fontSize: 12,
    italic: true,
    color: "486581",
    align: "center",
  });

  finalizeSlide(slide);
}

// Slide 3
{
  const slide = pptx.addSlide();
  addHeader(slide, "Core Results", "Inflation robust, GDP weak");
  addDivider(slide, 1.03);

  slide.addChart(
    pptx.ChartType.bar,
    [
      {
        name: "Inflation coefficient",
        labels: ["FE baseline", "IV external"],
        values: [metrics.feInflation, metrics.ivInflation],
      },
      {
        name: "GDP-growth coefficient",
        labels: ["FE baseline", "IV external"],
        values: [metrics.feGdp, metrics.ivGdp],
      },
    ],
    {
      x: 0.75,
      y: 1.42,
      w: 6.8,
      h: 4.8,
      barDir: "col",
      barGrouping: "clustered",
      showLegend: true,
      legendPos: "b",
      showValAxisTitle: true,
      valAxisTitle: "Estimated coefficient on money growth",
      valGridLine: { color: "DFE3E8", pt: 0.75 },
      chartColors: ["2D6AA6", "E07A5F"],
      fontFace: "Aptos",
      fontSize: 10,
    }
  );

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 7.9,
    y: 1.42,
    w: 4.75,
    h: 4.8,
    rectRadius: 0.05,
    fill: { color: "FFFFFF" },
    line: { color: "D5DCE6", pt: 1 },
  });
  slide.addText("Interpretation", {
    x: 8.2,
    y: 1.7,
    w: 3.0,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText(
    `Inflation:\n- Positive across major specs.\n- Significant on primary LP-IV horizons: ${metrics.inflationSigHorizons}.\n\nGDP growth:\n- Effects remain weak.\n- Significant primary LP-IV horizons: ${metrics.gdpSigHorizons}.\n\nIV quality:\n- Preferred first-stage stat: ${metrics.firstStageStat.toFixed(2)} (chi2(1)).`,
    {
      x: 8.2,
      y: 2.1,
      w: 4.15,
      h: 3.85,
      fontSize: 14,
      color: "102A43",
      valign: "top",
      lineSpacingMultiple: 1.15,
    }
  );

  finalizeSlide(slide);
}

// Slide 4
{
  const slide = pptx.addSlide();
  addHeader(slide, "Policy Implications and Claim Boundary", "No over-claiming");
  addDivider(slide, 1.03);

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.7,
    y: 1.35,
    w: 5.85,
    h: 4.9,
    rectRadius: 0.05,
    fill: { color: "E9F7EF" },
    line: { color: "B8E0C8", pt: 1 },
  });
  slide.addText("What policy teams can use now", {
    x: 1.0,
    y: 1.66,
    w: 5.1,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: "1E5631",
  });
  slide.addText(
    "1. Use money growth as an inflation-risk signal.\n2. Do not rely on this evidence to promise GDP acceleration.\n3. Combine cross-country estimates with country institutions and regime context.",
    {
      x: 1.0,
      y: 2.07,
      w: 5.2,
      h: 3.9,
      fontSize: 14,
      color: "1D3C2E",
      valign: "top",
      lineSpacingMultiple: 1.16,
    }
  );

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 6.85,
    y: 1.35,
    w: 5.8,
    h: 4.9,
    rectRadius: 0.05,
    fill: { color: "FDEBEC" },
    line: { color: "F2C1C4", pt: 1 },
  });
  slide.addText("What this project does not claim", {
    x: 7.15,
    y: 1.66,
    w: 5.1,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: "8A1C2B",
  });
  slide.addText(
    "- Not a universal causal elasticity.\n- Not policy certainty for every country and episode.\n- Not sufficient alone for growth-targeting strategy.\n\nReason: first-stage strength remains limited and identification is still the bottleneck.",
    {
      x: 7.15,
      y: 2.07,
      w: 5.15,
      h: 3.95,
      fontSize: 14,
      color: "5B1A1A",
      valign: "top",
      lineSpacingMultiple: 1.14,
    }
  );

  finalizeSlide(slide);
}

// Slide 5
{
  const slide = pptx.addSlide();
  addHeader(slide, "Next Research Agenda", "If moving to optional Phase 3");
  addDivider(slide, 1.03);

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.85,
    y: 1.45,
    w: 12.0,
    h: 3.95,
    rectRadius: 0.05,
    fill: { color: "FFFFFF" },
    line: { color: "D5DCE6", pt: 1 },
  });

  slide.addText("Identification-first roadmap", {
    x: 1.15,
    y: 1.76,
    w: 4.2,
    h: 0.38,
    fontSize: 15,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText(
    "1. Event/regime shocks (monetary reforms, mandate shifts).\n2. Heterogeneity by inflation regime and crisis state.\n3. Institution-aware exclusion logic.\n4. Fewer specs, stronger design, tighter causal scope.",
    {
      x: 1.15,
      y: 2.18,
      w: 5.75,
      h: 2.95,
      fontSize: 14,
      color: "102A43",
      valign: "top",
      lineSpacingMultiple: 1.15,
    }
  );

  slide.addShape(pptx.ShapeType.line, {
    x: 6.85,
    y: 1.9,
    w: 0,
    h: 3.0,
    line: { color: "D5DCE6", pt: 1 },
  });

  slide.addText("Closeout recommendation", {
    x: 7.25,
    y: 1.76,
    w: 3.7,
    h: 0.38,
    fontSize: 15,
    bold: true,
    color: "1E3A5F",
  });
  slide.addText("Closed (Phase Complete, Next Phase Optional)", {
    x: 7.25,
    y: 2.28,
    w: 5.2,
    h: 0.65,
    fontSize: 19,
    bold: true,
    color: "0B6E4F",
    valign: "mid",
  });
  slide.addText(
    `Portfolio message: disciplined econometrics, clear claim boundary, and a practical next-step agenda.\n\nPrimary first-stage mean (LP): ${metrics.meanFirstStagePrimary.toFixed(2)}.`,
    {
      x: 7.25,
      y: 3.08,
      w: 4.95,
      h: 1.8,
      fontSize: 13,
      color: "334E68",
      valign: "top",
      lineSpacingMultiple: 1.14,
    }
  );

  slide.addText(`Date: ${dateLabel}`, {
    x: 0.9,
    y: 6.77,
    w: 12.0,
    h: 0.28,
    fontSize: 11,
    color: "627D98",
    align: "right",
  });

  finalizeSlide(slide);
}

const outPath = path.resolve(__dirname, `ECON_INTERVIEW_DECK_${dateLabel}.pptx`);
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(`Deck written: ${outPath}`);
});
