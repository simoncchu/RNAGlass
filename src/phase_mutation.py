import sys
#sf_mut: is the mutation

def phase_mutation(sf_mut, sf_dipcall_rslt, sf_out):
    #1. first load in mutations
    m_mut={}
    with open(sf_mut) as fin_mut:
        for line in fin_mut:
            if len(line)>0 and line[0]=="#":
                continue
            fields=line.rstrip().split()
            s_chrm=fields[0]
            s_pos=fields[1]
            s_ref = fields[3]
            s_alt = fields[4]
            sid = s_chrm + "_" + s_pos + "_" + s_ref + "_" + s_alt
            m_mut[sid]=line.rstrip()

    #2. check overlap with dipcall results
    with open(sf_dipcall_rslt) as fin_dipcall, open(sf_out,"w") as fout:
        for line in fin_dipcall:
            if len(line)>0 and line[0]=="#":
                continue
            fields=line.rstrip().split()
            s_chrm=fields[0]
            s_pos=fields[1]
            s_ref=fields[3]
            s_alt=fields[4]
            s_filter=fields[6]
            s_hap="H1"
            if "GAP1" in s_filter:
                s_hap="H2"
            elif s_filter==".":
                s_hap="H1_H2"

            sid=s_chrm+"_"+s_pos+"_"+s_ref+"_"+s_alt
            if sid in m_mut:
                fout.write(m_mut[sid]+"\t"+s_hap+"\n")

if __name__ == '__main__':
    sf_mut=sys.argv[1]
    sf_dipcall_rslt=sys.argv[2]
    sf_out=sys.argv[3]
    phase_mutation(sf_mut, sf_dipcall_rslt, sf_out)