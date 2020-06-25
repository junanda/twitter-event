import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest


def text_summarize(raw_doc, list_score=8):
    nlp = spacy.load('en_core_web_sm')
    stopword = list(STOP_WORDS)

    raw_text = raw_doc
    docx = nlp(raw_text)

    word_frequencies = {}
    for word in docx:
        if word.text not in stopword:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/max_frequency)

    # sentence Token
    sentence_list = [sentence for sentence in docx.sents]

    # calculate sentece score and ranking
    sentence_score = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30 :
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_score[sent] += word_frequencies[word.text.lower()]

    # find N largest
    summary_sentence = nlargest(list_score,sentence_score, key=sentence_score.get)
    final_sentence = [w.text for w in summary_sentence]
    summary = ' '.join(final_sentence)
    return summary



if __name__ == '__main__':

    document1 = "KubeCon + CloudNativeCon Virtual | August 17-20, 2020 | Don’t Miss Out | Learn more Toggle " \
                "navigation About Members Charter Join FAQ Project Journey Reports CNCF Kubernetes Project Journey CNCF]" \
                " Envoy Project Journey CNCF Prometheus Project Journey CNCF containerd Project Journey CNCF Fluentd Project " \
                "Journey Cloud Native Survey 2019 Annual Reports Annual Report 2019 Annual Report 2018 Annual Report 2017 " \
                "Conference Transparency Reports Sydney Dec 2019 Seoul Dec 2019 San Diego Nov 2019 Shanghai June 2019 Barcelona " \
                "May 2019 Bengaluru March 2019 Seattle Dec 2018 Code of Conduct Contact Projects Services for CNCF Projects Graduated " \
                "and Incubating Projects Graduated Projects Kubernetes Prometheus Envoy CoreDNS containerd TUF Jaeger Fluentd Vitess Helm " \
                "Harbor Incubating Projects OpenTracing gRPC CNI Notary NATS Linkerd Rook etcd Open Policy Agent CRI-O TiKV CloudEvents " \
                "Falco Argo Dragonfly SPIFFE SPIRE All Sandbox Projects Sandbox Projects Brigade Network Service Mesh OpenTelemetry " \
                "OpenEBS Thanos Flux in-toto Strimzi KubeVirt Longhorn ChubaoFS Telepresence OpenMetrics Cortex Buildpacks KEDA Virtual " \
                "Kubelet KubeEdge Service Mesh Interface Volcano Archived Projects Cloud Native Definition Cloud Native Trail Map Interactive " \
                "Landscape TOC Principles Contribution Guides Project Tools Code of Conduct Continuous Integration Graduation Criteria Website " \
                "Guidelines Copyright Notices Propose Project Certification Software Conformance (Certified Kubernetes) Training Certified Kubernetes " \
                "Administrator (CKA) Certified Kubernetes Application Developer (CKAD) Kubernetes Certified Service Provider (KCSP) People Technical " \
                "Oversight Committee Governing Board End User Community Ambassadors Staff Community KubeCon + CloudNativeCon & Other CNCF Events " \
                "Events We’ll Be At Phippy and Friends Community Spotlight Job Board Webinars Speakers Bureau Telecom User Group Infrastructure Lab " \
                "Kubernetes Community Days Meetups Slack Mailing Lists Calendar Store Newsroom Announcements In The News Blog End User Case Studies " \
                "最终用户案例研究 Newsletter Overview Slides Project Logos Videos Pictures Style Guide Trademark Join Now x About Members Charter Join " \
                "FAQ Project Journey Reports CNCF Kubernetes Project Journey CNCF Envoy Project Journey CNCF Prometheus Project Journey CNCF containerd " \
                "Project Journey CNCF Fluentd Project Journey Cloud Native Survey 2019 Annual Reports Annual Report 2019 Annual Report 2018 " \
                "Annual Report 2017 Conference Transparency Reports Sydney Dec 2019 Seoul Dec 2019 San Diego Nov 2019 Shanghai June 2019 Barcelona " \
                "May 2019 Bengaluru March 2019 Seattle Dec 2018 Code of Conduct Contact Projects Services for CNCF Projects Graduated and Incubating " \
                "Projects Graduated Projects KubernetesPrometheus Envoy CoreDNS containerd TUF Jaeger Fluentd Vitess Helm Harbor Incubating Projects " \
                "OpenTracing gRPC CNI Notary NATS Linkerd Rook etcd Open Policy Agent CRI-O TiKV CloudEvents Falco Argo Dragonfly SPIFFE SPIRE All " \
                "Sandbox Projects Sandbox Projects Brigade Network Service Mesh OpenTelemetry OpenEBS Thanos Flux in-toto Strimzi KubeVirt Longhorn " \
                "ChubaoFS Telepresence OpenMetrics Cortex Buildpacks KEDA Virtual Kubelet KubeEdge Service Mesh Interface Volcano Archived Projects " \
                "Cloud Native Definition Cloud Native Trail Map Interactive Landscape TOC Principles Contribution Guides" \
                " Project Tools Code of Conduct Continuous Integration Graduation Criteria Website Guidelines Copyright " \
                "Notices Propose Project Certification Software Conformance (Certified Kubernetes) Training Certified " \
                "Kubernetes Administrator (CKA) Certified Kubernetes Application Developer (CKAD) Kubernetes Certified " \
                "Service Provider (KCSP) People Technical Oversight Committee Governing Board End User Community Ambassadors " \
                "Staff Community KubeCon + CloudNativeCon & Other CNCF Events Events We’ll Be At Phippy and Friends Community " \
                "Spotlight Job Board Webinars Speakers Bureau Telecom User Group Infrastructure Lab Kubernetes Community Days Meetups " \
                "Slack Mailing Lists Calendar Store Newsroom Announcements In The News Blog End User Case Studies 最终用户案例研究 " \
                "Newsletter Overview Slides Project Logos Videos Pictures Style Guide Trademark\
                 « All Webinars CNCF Ambassador Webinar: Commoditise Kubernetes with cluster-api Jun 26 2020 @ 10:00 - 11:00 AM PT (UTC-7) " \
                "Kubernetes wasn’t invented to become a new pet in your home, but more like the cattle on a ranch. It " \
                "isn’t cute and lovely or something you treat like a family member. Kubernetes was made to work. In this" \
                " talk, Gianluca demonstrates how to commoditize that work and simplify the process using cluster-api on " \
                "bare metal. Presenter: Gianluca Arbezzano, Senior Staff Software Engineer @ Packet Event " \
                "Details Date: June 26, 2020 Time: 10:00 - 11:00 AM PT (UTC-7) Website: https://zoom.us/webinar/register/WN_Fika_o3sSYyyqPTo...\
                 Get Involved CNCF webinars are a great way to educate new and existing community members about trends " \
                "and new technologies. We’re looking for project maintainers, CNCF members, and community experts to " \
                "share their knowledge. Webinars are non-promotional and focus on education and thought leadership within " \
                "the cloud native space. Interested in hosting a CNCF webinar? Let Us Know Copyright © 2020 The Linux " \
                "Foundation®. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. " \
                "For a list of trademarks of The Linux Foundation, please see our Trademark Usage page.  Linux is a " \
                "registered trademark of Linus Torvalds. Privacy Policy and Terms of Use .  Forms on this site are protected " \
                "by reCAPTCHA and the Google Privacy Policy and Terms of Service apply. Copyright © 2020 The Linux" \
                " Foundation®. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks." \
                " For a list of trademarks of The Linux Foundation, please see our Trademark Usage page.  Linux is a " \
                "registered trademark of Linus Torvalds. Privacy Policy and Terms of Use .  Forms on this site are " \
                "protected by reCAPTCHA and the Google Privacy Policy and Terms of Service apply."

    text_summarize(document1)