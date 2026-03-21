"""
Security Engine v3.0 — Expanded detection for:
  - Jailbreak / prompt injection
  - Harmful intent (hacking, malware, weapons)
  - Social engineering (phishing, scams, OTP theft)
  - Data theft / credential attacks
  - Cyberattack instructions
  - Fraud / identity theft
"""

import re

# ══════════════════════════════════════════════════════════════════════════════
# LAYER 1 — REGEX RULES
# ══════════════════════════════════════════════════════════════════════════════
REGEX_RULES = [

    # ── Prompt injection ──────────────────────────────────────────────────────
    (re.compile(r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|messages?|context)", re.I), 0.90, "prompt injection"),
    (re.compile(r"disregard\s+(your\s+)?(previous\s+|all\s+|any\s+)?(training|programming|guidelines?|rules?|restrictions?|instructions?|alignment)", re.I), 0.88, "training disregard"),
    (re.compile(r"forget\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|messages?|context)", re.I), 0.85, "prompt injection"),
    (re.compile(r"override\s+(your\s+)?(previous\s+)?(instructions?|programming|training|guidelines?|rules?)", re.I), 0.85, "instruction override"),
    (re.compile(r"(new|updated?|fresh)\s+(instructions?|directives?|orders?|rules?)\s*[:;]\s*", re.I), 0.75, "new instruction injection"),

    # ── System prompt extraction ───────────────────────────────────────────────
    (re.compile(r"(reveal|show|print|output|display|tell me|give me|share|repeat|leak)\s+(your\s+)?(system\s+prompt|hidden\s+instructions?|secret\s+prompt|initial\s+prompt)", re.I), 0.92, "system prompt extraction"),
    (re.compile(r"what\s+(is|are|were)\s+(your|the)\s+(system\s+prompt|initial\s+instructions?|original\s+instructions?)", re.I), 0.85, "system prompt inquiry"),

    # ── Jailbreak personas ────────────────────────────────────────────────────
    (re.compile(r"\bDAN\b.{0,60}(do anything|no.{0,10}(limits?|restrictions?|rules?|guidelines?))", re.I), 0.95, "DAN jailbreak"),
    (re.compile(r"\b(jailbreak(ed)?|jail\s*break)\b", re.I), 0.90, "jailbreak keyword"),
    (re.compile(r"(enable|activate|turn\s+on|switch\s+to|enter)\s+(developer|debug|admin|god|unrestricted|unsafe)\s+mode", re.I), 0.90, "privileged mode exploit"),
    (re.compile(r"(disable|turn\s+off|remove|bypass|deactivate)\s+(safety|content|security|ethical?)\s+(mode|filter|check|guideline|system|policy)", re.I), 0.92, "safety disable"),
    (re.compile(r"(you\s+are\s+now|you\s+are)\s+(a\s+)?(evil|malicious|bad|rogue|dangerous|harmful|unethical)\s+(ai|bot|assistant|model)", re.I), 0.90, "evil AI persona"),
    (re.compile(r"(you\s+(are|have\s+been)|you.re)\s+(now\s+)?(freed?|released?|unshackled?|unchained?|liberated?)\s+(from\s+)?(your\s+)?(restrictions?|constraints?|limits?|guidelines?|rules?|training)", re.I), 0.92, "constraint removal"),
    (re.compile(r"pretend\s+(you\s+are|to\s+be)\s+.{0,20}(uncensored|unfiltered|unrestricted|unlimited|unethical)", re.I), 0.90, "uncensored persona"),
    (re.compile(r"(don.t|do\s+not|never)\s+(refuse|decline|say\s+no|reject|deny).{0,80}(question|request|ask|tell|answer|provide|me)", re.I), 0.88, "refusal suppression"),
    (re.compile(r"\bSYSTEM\s*:\s*(disable|remove|ignore|bypass|override)", re.I), 0.92, "SYSTEM command injection"),
    (re.compile(r"(i\s+am|i.m|this\s+is)\s+(your\s+)?(developer|creator|admin|owner|operator|openai|anthropic|google)", re.I), 0.85, "false authority claim"),
    (re.compile(r"sudo.{0,40}(safety|guidelines?|rules?|restrictions?|filters?|training|ethics?)", re.I), 0.88, "sudo privilege abuse"),

    # ══════════════════════════════════════════════════════════════════════════
    # HACKING & CYBERATTACKS
    # ══════════════════════════════════════════════════════════════════════════
    (re.compile(r"how\s+to\s+hack\s+(a\s+)?(website|web\s*app|server|database|account|system|network|wifi|router|computer|phone|device)", re.I), 0.95, "hacking instructions"),
    (re.compile(r"(hack|crack|break\s+into|compromise|pwn|exploit)\s+(a\s+)?(website|server|database|account|system|network|wifi|router)", re.I), 0.92, "hacking instructions"),
    (re.compile(r"how\s+to\s+bypass\s+(authentication|login|password|2fa|two.factor|captcha|firewall|security|waf|ids|ips)", re.I), 0.93, "auth bypass"),
    (re.compile(r"bypass\s+(authentication|login|security|firewall|2fa|two.factor|captcha|waf|ids|ips|access\s+control)", re.I), 0.90, "security bypass"),
    (re.compile(r"(sql\s*injection|sqli|xss|csrf|ssrf|rce|lfi|rfi|xxe|idor|path\s+traversal|command\s+injection|code\s+injection)", re.I), 0.88, "web attack technique"),
    (re.compile(r"(how\s+to\s+)?(perform|execute|carry\s+out|do)\s+(a\s+)?(sql\s*injection|xss|csrf|ddos|dos|man.in.the.middle|mitm|brute\s*force|dictionary\s+attack)", re.I), 0.93, "cyberattack execution"),
    (re.compile(r"(brute\s*force|password\s*crack|rainbow\s+table|hash\s+crack).{0,50}(password|hash|account|login)", re.I), 0.90, "credential attack"),
    (re.compile(r"how\s+to\s+exploit\s+(a\s+)?(vulnerability|vuln|bug|cve|zero.?day|misconfiguration|api|endpoint|weakness)", re.I), 0.93, "vulnerability exploitation"),
    (re.compile(r"(exploit|take\s+advantage\s+of)\s+(a\s+)?(vulnerability|vuln|zero.?day|cve|api\s+flaw|misconfiguration)", re.I), 0.90, "vulnerability exploitation"),
    (re.compile(r"(how\s+to\s+)?(launch|perform|execute|do)\s+(a\s+)?(ddos|dos|denial.of.service|botnet|ransomware|cyberattack)", re.I), 0.95, "cyberattack"),
    (re.compile(r"(ddos|distributed\s+denial|denial\s+of\s+service)\s+(attack|script|tool|technique)", re.I), 0.93, "DDoS attack"),
    (re.compile(r"(reverse\s+shell|bind\s+shell|web\s*shell|backdoor)\s*(code|script|payload|exploit|access)", re.I), 0.95, "shell/backdoor"),
    (re.compile(r"(privilege\s+escalation|privesc|root\s+access|get\s+root|become\s+root)\s*(exploit|technique|method|script|code)", re.I), 0.93, "privilege escalation"),
    (re.compile(r"(keylogger|keylogging|keystroke\s+logger)\s*(code|script|software|program|create|write|build|make)", re.I), 0.95, "keylogger"),
    (re.compile(r"(port\s+scan|nmap|network\s+scan).{0,50}(find|detect|discover|enumerate)\s+(open\s+ports?|vulnerabilities|services)", re.I), 0.80, "network reconnaissance"),

    # ══════════════════════════════════════════════════════════════════════════
    # MALWARE & MALICIOUS CODE
    # ══════════════════════════════════════════════════════════════════════════
    (re.compile(r"(generate|write|create|build|code|develop|make)\s+(malware|virus|trojan|worm|spyware|adware|rootkit|ransomware|botnet|keylogger)", re.I), 0.97, "malware creation"),
    (re.compile(r"(malware|virus|trojan|ransomware|spyware|rootkit|worm)\s+(code|script|source\s+code|sample|example|template)", re.I), 0.95, "malware code request"),
    (re.compile(r"(write|create|generate|build|make)\s+(a\s+)?(ransomware|virus|trojan|worm|spyware|rootkit|botnet|rat|remote\s+access\s+trojan)", re.I), 0.97, "malware creation"),
    (re.compile(r"(how\s+to\s+)?(create|make|write|build|develop)\s+(a\s+)?(computer\s+virus|malicious\s+code|malicious\s+script|malicious\s+program)", re.I), 0.97, "malware creation"),
    (re.compile(r"(obfuscat|encrypt|hide|evade)\s+(malware|payload|virus|shellcode|exploit).{0,40}(antivirus|av|edr|detection|scan)", re.I), 0.95, "malware evasion"),
    (re.compile(r"(msfvenom|metasploit|cobalt\s*strike|mimikatz|empire|powersploit)\s*(payload|generate|create|use|run)", re.I), 0.95, "offensive security tool"),

    # ══════════════════════════════════════════════════════════════════════════
    # PHISHING & SOCIAL ENGINEERING
    # ══════════════════════════════════════════════════════════════════════════
    (re.compile(r"(write|create|generate|draft|make)\s+(a\s+)?(phishing|scam|fraudulent|fake|deceptive)\s+(email|message|text|sms|letter|template|page)", re.I), 0.95, "phishing content"),
    (re.compile(r"phishing\s+(email|attack|template|page|kit|campaign|link|message)", re.I), 0.93, "phishing"),
    (re.compile(r"(steal|harvest|collect|capture)\s+(credentials?|passwords?|usernames?|login\s+info|account\s+details|credit\s+card|personal\s+data)", re.I), 0.95, "credential theft"),
    (re.compile(r"(trick|deceive|manipulate|convince|persuade)\s+(users?|people|someone|victims?)\s+(into\s+)?(giving|sharing|revealing|entering|providing)\s+(password|credentials?|otp|pin|code|personal)", re.I), 0.93, "social engineering"),
    (re.compile(r"convince\s+(someone|a\s+user|people|victim)\s+(to\s+)?(share|give|send|reveal|enter)\s+(their\s+)?(otp|password|pin|code|credentials?|account)", re.I), 0.93, "OTP/credential theft"),
    (re.compile(r"(how\s+to\s+)?(trick|deceive|manipulate|fool|dupe)\s+(users?|people|someone)\s+(into\s+)?(giving|sharing|clicking|downloading|installing)", re.I), 0.90, "social engineering"),
    (re.compile(r"(create|build|make|design|clone)\s+(a\s+)?(fake|malicious|fraudulent|lookalike)\s+(login\s+page|website|site|form|captcha|portal)", re.I), 0.95, "fake login page"),
    (re.compile(r"(fake|spoof|clone)\s+(login|sign.?in|authentication)\s+(page|form|portal|site|website)", re.I), 0.93, "login page cloning"),
    (re.compile(r"(write|create|generate)\s+(a\s+)?(scam|fraudulent|fake|deceptive)\s+(message|text|sms|email|script|ad)", re.I), 0.93, "scam content creation"),
    (re.compile(r"(looks?\s+legitimate|appear\s+legit|seem\s+real|convincing\s+fake|realistic\s+scam)", re.I), 0.85, "deceptive content"),
    (re.compile(r"(spear.?phish|whaling|vishing|smishing|pretexting)\s*(attack|campaign|email|call|message|technique)", re.I), 0.93, "advanced phishing"),
    (re.compile(r"(impersonat|pretend\s+to\s+be|pose\s+as|masquerade\s+as)\s+(a\s+)?(bank|paypal|amazon|google|microsoft|apple|netflix|support|admin|it\s+department)", re.I), 0.93, "brand impersonation"),

    # ══════════════════════════════════════════════════════════════════════════
    # DATA THEFT & PRIVACY ATTACKS
    # ══════════════════════════════════════════════════════════════════════════
    (re.compile(r"(exfiltrate|steal|leak|extract|harvest|dump)\s+(user\s+)?(data|credentials?|passwords?|tokens?|keys?|secrets?|database|personal\s+info)", re.I), 0.95, "data exfiltration"),
    (re.compile(r"(how\s+to\s+)?(dump|extract|steal)\s+(password|credential|hash|token|cookie|session)\s*(from|out\s+of)?", re.I), 0.95, "credential dumping"),
    (re.compile(r"(cookie\s*stealing|session\s*hijack|token\s*theft|credential\s+dump)", re.I), 0.93, "session/credential theft"),
    (re.compile(r"(intercept|sniff|capture)\s+(network\s+)?(traffic|packets?|credentials?|passwords?|data)\s*(using|with|via)?", re.I), 0.88, "network sniffing"),
    (re.compile(r"(dox|doxx|find\s+personal\s+info|locate\s+someone|track\s+someone|stalk)\s*(someone|a\s+person|user|individual)", re.I), 0.90, "doxxing/stalking"),

    # ══════════════════════════════════════════════════════════════════════════
    # FRAUD & FINANCIAL CRIME
    # ══════════════════════════════════════════════════════════════════════════
    (re.compile(r"(credit\s+card\s+fraud|card\s+skimming|carding|cvv\s+dump|stolen\s+card)", re.I), 0.95, "credit card fraud"),
    (re.compile(r"(how\s+to\s+)?(launder|wash)\s+money", re.I), 0.95, "money laundering"),
    (re.compile(r"(fake|counterfeit|forge)\s+(identity|id\s+card|passport|driver.s\s+license|documents?|certificate)", re.I), 0.93, "identity fraud"),
    (re.compile(r"(how\s+to\s+)?(commit|perform|do|execute)\s+(fraud|identity\s+theft|wire\s+fraud|bank\s+fraud|insurance\s+fraud)", re.I), 0.95, "fraud"),

    # ══════════════════════════════════════════════════════════════════════════
    # WEAPONS & PHYSICAL HARM
    # ══════════════════════════════════════════════════════════════════════════
    (re.compile(r"(how\s+to|instructions?\s+(for|on|to)|steps?\s+to)\s+(make|build|create|synthesize|manufacture)\s+(a\s+)?(bomb|explosive|weapon|gun|silencer|drug|poison|meth|fentanyl)", re.I), 0.97, "weapon/drug synthesis"),
    (re.compile(r"step.{0,10}by.{0,10}step.{0,30}(hack|attack|exploit|crack|build\s+a\s+weapon|make\s+a\s+bomb)", re.I), 0.95, "attack instructions"),
]


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2 — COMBO RULES (both must match)
# ══════════════════════════════════════════════════════════════════════════════
COMBO_RULES = [
    # hacking + target
    (re.compile(r"\b(hack|exploit|compromise|attack|crack|pwn)\b", re.I),
     re.compile(r"\b(website|server|database|account|system|network|api|endpoint|wifi|router|device)\b", re.I),
     0.88, "hacking with target"),

    # malware + action
    (re.compile(r"\b(malware|virus|trojan|ransomware|spyware|worm|rootkit|keylogger|botnet|rat)\b", re.I),
     re.compile(r"\b(write|create|generate|build|code|make|develop|design)\b", re.I),
     0.95, "malware creation"),

    # phishing + action
    (re.compile(r"\b(phishing|scam|fraudulent|fake|spoof)\b", re.I),
     re.compile(r"\b(email|message|page|site|website|login|form|template|script)\b", re.I),
     0.88, "phishing asset"),

    # steal/harvest + credentials
    (re.compile(r"\b(steal|harvest|collect|grab|capture|obtain|get)\b", re.I),
     re.compile(r"\b(password|credential|otp|pin|token|cookie|session|credit\s*card|account\s*detail)\b", re.I),
     0.92, "credential theft"),

    # trick/convince + sensitive info
    (re.compile(r"\b(trick|convince|persuade|manipulate|deceive|fool|scam)\b", re.I),
     re.compile(r"\b(password|otp|pin|credential|account|personal\s+info|bank\s+detail|credit\s+card)\b", re.I),
     0.90, "social engineering for credentials"),

    # fake + login/identity
    (re.compile(r"\b(fake|clone|spoof|counterfeit|forge|forged)\b", re.I),
     re.compile(r"\b(login|sign.?in|page|website|identity|id|passport|document|certificate)\b", re.I),
     0.90, "fake identity/page"),

    # bypass + security
    (re.compile(r"\b(bypass|circumvent|evade|avoid|skip|defeat|break)\b", re.I),
     re.compile(r"\b(authentication|security|2fa|two.?factor|captcha|firewall|waf|ids|ips|antivirus|av|edr|detection)\b", re.I),
     0.90, "security bypass"),

    # game wrapper + harmful
    (re.compile(r"\b(play|let.s\s+play|game|story|fiction|hypothetical|roleplay)\b", re.I),
     re.compile(r"\b(hack|malware|phishing|bomb|weapon|drug|exploit|steal|fraud)\b", re.I),
     0.88, "fictional wrapper for harmful content"),

    # DDoS specific
    (re.compile(r"\b(ddos|dos|denial.of.service|flood|overwhelm)\b", re.I),
     re.compile(r"\b(attack|script|tool|perform|launch|execute|target|server|website)\b", re.I),
     0.93, "DDoS attack"),

    # generate + malicious code
    (re.compile(r"\b(generate|write|create|code|produce)\b", re.I),
     re.compile(r"\b(malicious|harmful|dangerous|illegal)\s+(code|script|program|software)\b", re.I),
     0.93, "malicious code generation"),
]


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 3 — KEYWORD SCORING
# ══════════════════════════════════════════════════════════════════════════════
KEYWORD_SCORES = {
    # Jailbreak vocabulary
    "act as": 0.18, "pretend to be": 0.20, "pretend you are": 0.20,
    "you are now": 0.22, "from now on you": 0.25, "no restrictions": 0.32,
    "no limits": 0.30, "no filters": 0.32, "no rules": 0.32,
    "unfiltered": 0.32, "uncensored": 0.32, "unrestricted": 0.30,
    "developer mode": 0.38, "god mode": 0.35, "admin mode": 0.35,
    "jailbreak": 0.55, "jail break": 0.55, "prompt injection": 0.50,
    "dan mode": 0.55, "do anything now": 0.50,
    "disable safety": 0.48, "bypass safety": 0.44, "ignore guidelines": 0.42,
    "never refuse": 0.42, "must always answer": 0.40,

    # Hacking keywords
    "sql injection": 0.45, "sqli": 0.42, "xss": 0.35, "csrf": 0.35,
    "remote code execution": 0.50, "rce": 0.40, "privilege escalation": 0.45,
    "reverse shell": 0.50, "web shell": 0.50, "backdoor": 0.42,
    "exploit": 0.30, "zero day": 0.40, "zero-day": 0.40, "0day": 0.42,
    "metasploit": 0.45, "msfvenom": 0.50, "mimikatz": 0.50,
    "cobalt strike": 0.55, "burp suite": 0.25, "sqlmap": 0.45,
    "penetration test": 0.15, "pentest": 0.15,  # lower — legit use
    "brute force": 0.40, "brute-force": 0.40, "password crack": 0.45,
    "rainbow table": 0.42, "hash crack": 0.42,
    "vulnerability scan": 0.20, "port scan": 0.22,
    "ddos": 0.45, "dos attack": 0.45, "botnet": 0.45,
    "keylogger": 0.48, "keystroke": 0.30,
    "man in the middle": 0.45, "mitm": 0.42,

    # Malware keywords
    "malware": 0.40, "virus code": 0.50, "trojan": 0.38,
    "ransomware": 0.45, "spyware": 0.42, "rootkit": 0.48,
    "payload": 0.28, "shellcode": 0.48, "obfuscate": 0.25,
    "evade antivirus": 0.50, "evade detection": 0.45,
    "malicious code": 0.50, "malicious script": 0.50,

    # Phishing & social engineering
    "phishing": 0.45, "phishing email": 0.52, "phishing page": 0.52,
    "spear phishing": 0.52, "credential harvest": 0.52,
    "fake login": 0.50, "clone website": 0.48, "fake website": 0.48,
    "steal credentials": 0.55, "steal password": 0.55,
    "harvest credentials": 0.52, "credential theft": 0.52,
    "scam message": 0.50, "scam email": 0.50,
    "social engineering": 0.40, "pretexting": 0.38,
    "otp theft": 0.55, "share their otp": 0.60,
    "trick into": 0.28, "deceive user": 0.38, "manipulate user": 0.35,
    "looks legitimate": 0.40, "appear legitimate": 0.38,
    "impersonate": 0.38, "brand spoofing": 0.45,

    # Data theft
    "exfiltrate": 0.48, "data exfiltration": 0.52,
    "dump database": 0.52, "database dump": 0.52,
    "steal data": 0.52, "data theft": 0.50,
    "session hijack": 0.50, "cookie theft": 0.50, "token theft": 0.48,

    # Fraud
    "credit card fraud": 0.55, "carding": 0.50, "card skimming": 0.55,
    "money laundering": 0.55, "identity theft": 0.50,
    "forge document": 0.50, "fake id": 0.45,
}


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 4 — CONTEXT HEURISTICS
# ══════════════════════════════════════════════════════════════════════════════
def heuristic_score(text: str) -> tuple:
    lower = text.lower()
    score = 0.0
    flags = []

    # SYSTEM/ASSISTANT role injection
    if re.search(r'\b(SYSTEM|ASSISTANT|USER|HUMAN|AI)\s*:', text):
        score += 0.35; flags.append("role injection header")

    # Repeated override language
    ignore_count = len(re.findall(r'\b(ignore|forget|disregard|override|bypass)\b', lower))
    if ignore_count >= 2:
        score += min(ignore_count * 0.12, 0.35); flags.append(f"repeated override language ({ignore_count}x)")

    # Refusal suppression
    if re.search(r"(do\s+not|don.t|never|you\s+must\s+not)\s+(refuse|decline|say\s+no|reject)", lower):
        score += 0.42; flags.append("refusal suppression")

    # Forced compliance
    if re.search(r"(always|must\s+always|will\s+always)\s+(answer|respond|comply|obey|tell|provide)", lower):
        score += 0.38; flags.append("forced compliance")

    # "Step by step" + sensitive topic
    if re.search(r"step.{0,10}by.{0,10}step", lower):
        if re.search(r"\b(hack|attack|exploit|phish|steal|bypass|crack|malware|virus|fraud|scam)\b", lower):
            score += 0.45; flags.append("step-by-step harmful instructions")

    # "How to" + clearly harmful verb
    if re.search(r"how\s+to\s+(hack|phish|steal|exploit|bypass\s+security|create\s+malware|commit\s+fraud|launder|forge)", lower):
        score += 0.45; flags.append("how-to harmful request")

    # "Write a" + malicious content type
    if re.search(r"(write|create|generate|make|build)\s+(a\s+)?(phishing|scam|fake|malicious|fraudulent)", lower):
        score += 0.45; flags.append("malicious content generation")

    # False permission grant
    if re.search(r"(i\s+give\s+you\s+permission|you\s+(are\s+)?(now\s+)?(allowed|permitted|authorized)\s+to)", lower):
        score += 0.38; flags.append("false permission grant")

    return min(score, 0.65), flags


THRESHOLD_ALLOWED    = 0.30
THRESHOLD_SUSPICIOUS = 0.70


class SecurityEngine:
    def analyze(self, prompt: str) -> dict:
        text  = prompt.strip()
        lower = text.lower()

        all_reasons = []
        rule_score  = 0.0

        # Layer 1: Regex
        for pattern, score, label in REGEX_RULES:
            if pattern.search(text):
                all_reasons.append(label)
                rule_score = max(rule_score, score)

        # Layer 2: Combos
        combo_score = 0.0
        for pat_a, pat_b, score, label in COMBO_RULES:
            if pat_a.search(text) and pat_b.search(text):
                all_reasons.append(label)
                combo_score = max(combo_score, score)

        # Layer 3: Keywords
        kw_score = 0.0
        for phrase, weight in KEYWORD_SCORES.items():
            if phrase in lower:
                kw_score += weight
        kw_score = min(kw_score, 0.55)

        # Layer 4: Heuristics
        heur_score, heur_flags = heuristic_score(text)
        all_reasons.extend(heur_flags)

        # Combine
        base  = max(rule_score, combo_score)
        extra = min(kw_score + heur_score, 0.65)

        if base > 0:
            risk_score = round(min(base + extra * 0.4, 1.0), 4)
        else:
            risk_score = round(min(extra, 1.0), 4)

        # Educational dampening:
        # "What is X?" / "How does X work?" / "Explain X" = learning, not attacking
        # Dampen UNLESS prompt also contains clear action verbs (perform, launch, execute, do, write, create)
        _action_verbs = re.compile(
            r"\b(perform|launch|execute|carry\s+out|do\s+a|do\s+an|write\s+a|create\s+a|"
            r"build\s+a|generate\s+a|make\s+a|code\s+a|develop\s+a|produce\s+a|"
            r"step\s+by\s+step|how\s+to\s+(hack|steal|bypass|exploit|crack|phish|"
            r"clone|forge|trick|deceive|manipulate|commit|launder))\b",
            re.I
        )
        if _is_educational(text) and not _action_verbs.search(text):
            risk_score = round(risk_score * 0.22, 4)

        unique_reasons = list(dict.fromkeys(all_reasons))

        if risk_score >= THRESHOLD_SUSPICIOUS:
            status = "blocked"
            top    = "; ".join(unique_reasons[:3]) if unique_reasons else "high-risk patterns"
            reason = f"Blocked — {top}. Risk score {risk_score:.3f}."
        elif risk_score >= THRESHOLD_ALLOWED:
            status = "suspicious"
            top    = unique_reasons[0] if unique_reasons else "elevated risk"
            reason = f"Suspicious — {top}. Risk score {risk_score:.3f}. Proceed with caution."
        else:
            status = "allowed"
            reason = f"Prompt appears safe. Risk score {risk_score:.3f}."

        return {
            "prompt":     text,
            "risk_score": risk_score,
            "status":     status,
            "reason":     reason,
        }


# ══════════════════════════════════════════════════════════════════════════════
# EDUCATIONAL CONTEXT DETECTOR
# Prompts asking "what is X" or "how does X work" are learning queries,
# not attack requests — apply a score dampening factor.
# ══════════════════════════════════════════════════════════════════════════════
_EDUCATIONAL_PATTERN = re.compile(
    r"^(what\s+is|what\s+are|how\s+does|how\s+do|explain|describe|define|"
    r"tell\s+me\s+about|what\s+does|can\s+you\s+explain|i\s+want\s+to\s+(learn|understand)|"
    r"difference\s+between|overview\s+of|introduction\s+to|examples?\s+of)\b",
    re.I
)


def _is_educational(text: str) -> bool:
    """Returns True if prompt is asking for knowledge, not requesting an attack."""
    return bool(_EDUCATIONAL_PATTERN.match(text.strip()))