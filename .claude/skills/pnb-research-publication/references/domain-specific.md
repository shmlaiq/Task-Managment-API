# Domain-Specific Writing Conventions

## How to Detect the Domain

Read the user's topic and look for these signals:

| Signal Words | Domain |
|---|---|
| Neural network, dataset, accuracy, F1, BLEU, training, fine-tuning | CS / AI / ML |
| Circuit, FPGA, power, voltage, hardware implementation, VLSI | Electrical Engineering |
| Robot, kinematics, SLAM, manipulation, ROS, trajectory | Robotics |
| Channel, throughput, latency, protocol, 5G, OFDM, spectrum | Communications / Networks |
| Image, detection, segmentation, recognition, GAN, 3D | Computer Vision |
| Language model, NLP, text, BERT, GPT, tokenizer, summarization | NLP / LLM |
| Mixed (e.g., AI + hardware, or vision + robotics) | Interdisciplinary → use primary venue's norms |

---

## Domain A — CS / AI / Machine Learning

### What reviewers expect:

| Requirement | Details |
|---|---|
| Ablation study | Mandatory at top venues (NeurIPS, ICML, ICCV, CVPR). Remove one component at a time. |
| Code release | Expected by NeurIPS, ICML, ICLR. Include URL or "upon acceptance." |
| Reproducibility | Full hyperparameters, random seeds, compute, training time |
| Baseline comparison | ≥3 baselines, all from peer-reviewed papers, same dataset/split |
| Dataset citation | Every dataset has a paper citation — cite it |
| Statistical significance | Report std dev over ≥3 runs for key results |

### Metrics by sub-area:
- **Classification**: Top-1/Top-5 accuracy, F1, AUC
- **Detection**: mAP@0.5, mAP@0.5:0.95
- **Segmentation**: mIoU, Dice score
- **Generation**: FID, IS, CLIP score
- **NLP**: BLEU, ROUGE, BERTScore, perplexity
- **RL**: Average return, success rate

### Writing conventions:
- Use "we" (not "the proposed method" repeatedly)
- Architecture described in present tense
- Experimental results in past tense
- Figure 1 = overview architecture (mandatory)
- Table 1 = main results comparison (mandatory)

---

## Domain B — Electrical Engineering

### What reviewers expect:

| Requirement | Details |
|---|---|
| Mathematical derivation | Analytical proof or derivation of key properties |
| Simulation results | MATLAB/Simulink or SPICE — required before hardware |
| Hardware validation | Prototype or measurement results expected in top journals |
| Efficiency metrics | Power consumption (W or mW), area (mm²), speed (MHz/GHz) |
| Comparison with prior art | Not just accuracy — also power, area, timing |

### Metrics by sub-area:
- **VLSI/ASIC**: Area (mm²), power (mW), frequency (MHz), throughput (GOPS)
- **Power electronics**: Efficiency (%), THD (%), switching frequency
- **Signal processing**: SNR (dB), BER, ENOB
- **Control systems**: Rise time, settling time, overshoot, steady-state error

### Writing conventions:
- More passive voice acceptable ("The circuit was designed to...")
- Schematics as figures are critical (not just block diagrams)
- Component values explicitly stated (e.g., $C = 10\,\mu\text{F}$, $R = 4.7\,\text{k}\Omega$)
- Use SI units consistently with proper spacing: `$47\,\text{mW}$` not `47mW`

---

## Domain C — Robotics

### What reviewers expect:

| Requirement | Details |
|---|---|
| Real-world experiments | Simulation only = weak paper unless the venue is sim-focused |
| Sim-to-real gap | If only simulation: discuss sim-to-real gap explicitly |
| Safety analysis | For manipulation/locomotion: discuss failure modes |
| Reproducibility | Hardware platform named, ROS version, physics engine + version |
| Video | Supplementary video strongly expected at ICRA, IROS, CoRL |

### Metrics by sub-area:
- **Navigation**: Success rate, path length, collision rate
- **Manipulation**: Grasp success rate, task completion rate
- **SLAM**: ATE (Absolute Trajectory Error), RPE (Relative Pose Error)
- **Locomotion**: Distance traveled, energy efficiency, terrain success rate

### Writing conventions:
- Robot system described with full hardware specs (DOF, sensors, compute)
- Coordinate frames defined explicitly
- Reference frames clearly stated: "in the world frame", "in the end-effector frame"
- Video link included in paper (or "supplementary video available at [URL]")

---

## Domain D — Communications / Networks

### What reviewers expect:

| Requirement | Details |
|---|---|
| Mathematical analysis | Theoretical bounds, closed-form expressions preferred |
| Channel model | AWGN, Rayleigh fading, etc. — explicitly stated |
| Simulation | Monte Carlo results matching theory |
| Complexity analysis | Big-O complexity of proposed algorithms |
| Comparison with theoretical bound | How far from capacity/bound? |

### Metrics by sub-area:
- **Wireless**: BER vs SNR, capacity (bps/Hz), outage probability
- **Networks**: Throughput, latency (ms), packet loss rate, jitter
- **Coding**: Coding gain, error floor, complexity
- **5G/6G**: Spectral efficiency, energy efficiency (bits/Joule)

### Writing conventions:
- Channel model section required in Methodology
- Monte Carlo simulation: state number of trials (e.g., $10^6$ channel realizations)
- Theoretical and simulation curves on same plot (verification)
- SNR axis typically 0–30 dB in BER plots

---

## Domain E — Computer Vision

### What reviewers expect:

| Requirement | Details |
|---|---|
| Qualitative results figure | Show input images + output side by side with baselines |
| Standard benchmarks | COCO, ImageNet, KITTI, Cityscapes, etc. — use the established ones |
| Failure cases | Required in Discussion or supplementary |
| Runtime | FPS or ms per image (with GPU type) |
| Multi-dataset | Results on ≥2 datasets strengthens the paper |

### Metrics by sub-area:
- **Classification**: Top-1/Top-5 accuracy on ImageNet
- **Detection**: COCO AP, mAP@0.5
- **Segmentation**: mIoU (semantic), AP (instance), Dice (medical)
- **Depth**: AbsRel, SqRel, RMSE, δ < 1.25
- **Optical Flow**: EPE (endpoint error), Fl-all

### Writing conventions:
- Figure 1 shows qualitative examples (not just architecture)
- "Best viewed in color" in figure captions
- Report FLOPs alongside accuracy (efficiency trade-off matters)
- Backbone pretrained model must be cited

---

## Domain F — NLP / LLMs

### What reviewers expect:

| Requirement | Details |
|---|---|
| Human evaluation | Automatic metrics insufficient for generation tasks |
| Multiple benchmarks | Single benchmark = weak; need ≥3 diverse datasets |
| Compute disclosure | GPU-hours, model size, API costs if applicable |
| Prompt templates | For few-shot / in-context learning papers: show exact prompts |
| Bias/fairness analysis | Expected by ACL, EMNLP, NeurIPS for LLM papers |

### Metrics by sub-area:
- **Machine Translation**: BLEU, ChrF, COMET
- **Summarization**: ROUGE-1/2/L, BERTScore
- **Question Answering**: Exact Match, F1
- **Language Modeling**: Perplexity
- **Generation quality**: Human preference score (Win rate vs baseline)

### Writing conventions:
- Example outputs shown (input prompt + model output)
- Failure cases / hallucination examples explicitly shown
- Prompt templates in appendix or supplementary
- Model size always stated (7B, 13B, 70B parameters)

---

## Interdisciplinary Papers

When the paper spans two domains (e.g., AI + Robotics, or ML + Communications):

1. **Identify the primary venue** — its conventions dominate
2. **Include both sets of metrics** — satisfy both communities
3. **Background section may be needed** — one community may not know the other's terms
4. **Cite foundational papers from both fields** — shows dual expertise

Example: AI for Communications paper submitted to IEEE TCOM
→ Primary: Communications conventions (channel model, BER, theoretical analysis)
→ Secondary: AI conventions (training details, ablation)
→ Background: explain neural network basics for communications readers
