import pysam
from optparse import OptionParser
from x_gene_annotation import *

class mRNA_Transfer():

    def call_transfer_mut(self, sf_rna, sf_dna_up, sf_dna_bottom, sf_candidate):
        m_rna_vars = self.load_variants(sf_rna)
        m_DNA_RNA_ovlp_vars = self.get_overlap_variants(sf_dna_bottom, m_rna_vars)
        m_candidates = self.get_mut_exclusive_var(sf_dna_up, m_DNA_RNA_ovlp_vars)
        self.get_sub_var(sf_rna, m_candidates, sf_candidate)

    def load_variants(self, sf_vcfFile):
        vcf = pysam.VariantFile(sf_vcfFile)
        m_variants = {}
        for unique_id, var in enumerate(vcf.fetch()):
            chrm = var.chrom
            start = var.pos
            s_id = chrm + "~" + str(start) + "~" + str(var.ref) + "_" + str(var.alts[0])
            m_variants[s_id] = 1
        return m_variants

    def get_overlap_variants(self, sf_vcfFile, m_existing_vars):
        vcf = pysam.VariantFile(sf_vcfFile)
        m_variants = {}
        for unique_id, var in enumerate(vcf.fetch()):
            chrm = var.chrom
            start = var.pos
            s_id = chrm + "~" + str(start) + "~" + str(var.ref) + "_" + str(var.alts[0])
            if s_id in m_existing_vars:
                m_variants[s_id] = 1
        return m_variants

    def get_mut_exclusive_var(self, sf_vcfFile, m_existing_vars):
        vcf = pysam.VariantFile(sf_vcfFile)
        m_variants = {}
        for unique_id, var in enumerate(vcf.fetch()):
            chrm = var.chrom
            start = var.pos
            s_id = chrm + "~" + str(start) + "~" + str(var.ref) + "_" + str(var.alts[0])
            # if s_id not in m_existing_vars:
            m_variants[s_id] = 1

        m_mut_exc_var = {}
        for s_id in m_existing_vars:
            if s_id not in m_variants:
                m_mut_exc_var[s_id] = 1
        return m_mut_exc_var

    def get_sub_var(self, sf_vcfFile, m_existing_vars, sf_sub_vcf):
        vcf = pysam.VariantFile(sf_vcfFile)
        vcf_out = pysam.VariantFile(sf_sub_vcf, 'w', header=vcf.header)
        for unique_id, var in enumerate(vcf.fetch()):
            chrm = var.chrom
            start = var.pos
            s_id = chrm + "~" + str(start) + "~" + str(var.ref) + "_" + str(var.alts[0])
            if s_id in m_existing_vars:
                vcf_out.write(var)
####
####
##parse the options:
def parse_option():
    parser = OptionParser()

    parser.add_option("-p", "--path", dest="wfolder", type="string",
                      help="Working folder")
    parser.add_option("--gene", dest="gene", default="",
                      help="Gene Annotation file", metavar="FILE")
    parser.add_option("--rna", dest="rna",
                      help="RNA mutation vcf file ", metavar="FILE")
    parser.add_option("--phase", dest="phase",
                      help="Mutation phasing", metavar="FILE")
    parser.add_option("--dna_up", dest="dna_up",
                      help="DNA mutation file of scion", metavar="FILE")
    parser.add_option("--dna_bottom", dest="dna_bottom",
                      help="DNA mutation file of root ", metavar="FILE")
    parser.add_option("-c", dest="cutoff", type="int", default=0,
                      help="cutoff of minimum supporting reads")
    parser.add_option("-o", "--output", dest="output",
                      help="candidate mutation file", metavar="FILE")
    (options, args) = parser.parse_args()
    return (options, args)

####
if __name__ == '__main__':
    (options, args) = parse_option()

    sf_rna_mut=options.rna
    sf_dna_up=options.dna_up
    sf_dna_bottom=options.dna_bottom
    sf_candidates=options.output
    rna_transfer=mRNA_Transfer()
    rna_transfer.call_transfer_mut(sf_rna_mut, sf_dna_up, sf_dna_bottom, sf_candidates)

    sf_gene_annotation = options.gene
    UP_DOWN_GENE=1500
    if sf_gene_annotation !="":
        gff = GFF3(sf_gene_annotation)
        iextnd = UP_DOWN_GENE
        gff.load_gene_annotation_with_extnd(iextnd)
        gff.index_gene_annotation_interval_tree()
        gff.annotate_results(sf_candidates, sf_candidates+".with_gene_annotation")
####